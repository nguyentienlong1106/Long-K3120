import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import (
    commit_parse,
    find_object,
    find_tree_files,
    read_object,
    resolve_object,
    read_tree,
)
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    parent = resolve_head(gitdir)
    commit = commit_tree(gitdir, tree, message, parent, author)
    return commit


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for i in read_index(gitdir):
        if pathlib.Path(i.name).exists():
            os.remove(i.name)
    commit = commit_parse(read_object(obj_name, gitdir)[1])
    q = True
    while q:
        trees: tp.List[tp.Tuple[tp.List[tp.Tuple[int, str, str]], pathlib.Path]] = [
            (read_tree(read_object(commit["tree"], gitdir)[1]), gitdir.parent)
        ]
        while trees:
            tree_content, tree_path = trees.pop()
            for i in tree_content:
                fmt, data = read_object(i[2], gitdir)
                if fmt != "tree":
                    if not (tree_path / i[1]).exists():
                        with (tree_path / i[1]).open("wb") as f:
                            f.write(data)
                            (tree_path / i[1]).chmod(int(str(i[0]), 8))
                            f.close()
                else:
                    if not (tree_path / i[1]).exists():
                        (tree_path / i[1]).mkdir()
                    trees.append((read_tree(data), tree_path / i[1]))
        if "parent" in commit:
            commit = commit_parse((read_object(commit["parent"], gitdir)[1]))
        else:
            q = not q
    for i in gitdir.parent.glob("*"):
        if i.is_dir() and i != gitdir:
            try:
                os.removedirs(i)
            except OSError:
                continue
