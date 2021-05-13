import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    res = hashlib.sha1(store).hexdigest()
    if write:
        obj_dir = repo_find() / "objects" / res[0:2]
        if not obj_dir.exists():
            obj_dir.mkdir()
        with (obj_dir / res[2:]).open("wb") as file:
            file.write(zlib.compress((fmt + " " + str(len(data))).encode() + b"\00" + data))
    return res


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if 4 > len(obj_name) or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    obj_dir = gitdir / "objects"
    obj_list = []
    for file in (obj_dir / obj_name[0:2]).glob("*"):
        cur_obj_name = file.parent.name + file.name
        if obj_name == cur_obj_name[0: len(obj_name)]:
            obj_list.append(cur_obj_name)
    if not obj_list:
        raise Exception(f"Not a valid object name {obj_name}")
    return obj_list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    obj_path = find_object(sha, gitdir)
    cur_file = open(gitdir / "objects" / obj_path[0:2] / obj_path[2:], "rb")
    obj_data = zlib.decompress(cur_file.read())
    right, left = obj_data.find(b" "), obj_data.find(b"\x00")
    length = int(obj_data[right:left].decode("ascii"))
    content = obj_data[left + 1:]
    fmt = obj_data[0:right].decode()
    cur_file.close()
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []
    while data:
        start_sha = data.index(b"\00")
        mode_b: bytes
        name_b: bytes
        mode_b, name_b = data[0:start_sha].split(b" ")
        mode = mode_b.decode()
        name = name_b.decode()
        sha = data[start_sha + 1:start_sha + 21]
        tree.append((int(mode), name, sha.hex()))
        data = data[start_sha + 21:]
    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    if "GIT_DIR" not in os.environ:
        git_dir = pathlib.Path(".git")
    else:
        git_dir = pathlib.Path(os.environ["GIT_DIR"])
    fmt, data = read_object(obj_name, git_dir)
    blob_or_commit = ("blob", "commit")
    if fmt in blob_or_commit:
        print(data.decode())
    else:
        for tree in read_tree(data):
            if tree[0] != 40000:
                print("100644", "blob", tree[2] + "\t" + tree[1])
            else:
                print("040000", "tree", tree[2] + "\t" + tree[1])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, data = read_object(tree_sha, gitdir)
    objects = read_tree(data)
    res = []
    for i in objects:
        if i[0] == 100644 or i[0] == 100755:
            res.append((i[1], i[2]))
        else:
            sub_objects = find_tree_files(i[2], gitdir)
            for j in sub_objects:
                res.append((i[1] + "/" + j[0], j[1]))
    return res


def commit_parse(raw: bytes, start: int = 0, dct=None):
    res: tp.Dict[str, tp.Any] = {"message": []}
    for i in map(lambda x: x.decode(), raw.split(b"\n")):
        if "tree" in i or "parent" in i or "author" in i or "committer" in i:
            name, val = i.split(" ", maxsplit=1)
            res[name] = val
        else:
            res["message"].append(i)
    return res
