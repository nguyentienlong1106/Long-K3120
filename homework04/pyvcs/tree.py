import hashlib
import os
import pathlib
import datetime
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index, update_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_entries = []
    content: tp.List[tp.Tuple[int, str, bytes]] = []
    subtrees: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    for i in (gitdir.parent / dirname).glob("*"):
        tree_entries.append(str(i))
    for i in index:
        if i.name in tree_entries:
            content.append((i.mode, str(gitdir.parent / i.name), i.sha1))
        else:
            name = i.name.lstrip(dirname).split("/", 1)[0]
            if not name in subtrees:
                subtrees[name] = []
            subtrees[name].append(i)
    for i in subtrees:
        if dirname != "":
            content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / i),
                    bytes.fromhex(write_tree(gitdir, subtrees[i], dirname + "/" + i)),
                )
            )
        else:
            content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / i),
                    bytes.fromhex(write_tree(gitdir, subtrees[i], i)),
                )
            )
    content.sort(key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].split('/')[-1]}".encode() + b"\00" + elem[2] for elem in content
    )
    tree = hash_object(data, "tree", True)
    return tree

def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None,
) -> str:
    if author is None and "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ:
        author = (
                os.getenv("GIT_AUTHOR_NAME", None)
                + " "
                + f'<{os.getenv("GIT_AUTHOR_EMAIL", None)}>'
        )
    comtime = (
            str(int(time.mktime(time.localtime()))) + " " + str(time.strftime("%z", time.gmtime()))
    )
    content = (
            "tree "
            + tree
            + "\nauthor "
            + author
            + " "
            + comtime
            + "\ncommitter "
            + author
            + " "
            + comtime
            + "\n\n"
            + message
            + "\n"
    )
    sha = hash_object(content.encode(), "commit", True)
    return sha
