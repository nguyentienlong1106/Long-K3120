import pathlib
import typing as tp
import os


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:

    pathlib.Path(gitdir / ref).touch()
    with (gitdir / ref).open("w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with (gitdir / name).open("w") as file:
        file.write(ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    if (gitdir / refname).exists():
        with (gitdir / refname).open() as f:
            return f.read().strip()
    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, get_ref(gitdir))


def is_detached(gitdir: pathlib.Path) -> bool:
    if get_ref(gitdir) == "":
        return True
    return False


def get_ref(gitdir: pathlib.Path) -> str:
    with (gitdir / "HEAD").open("r") as head:
        data = head.read().strip().split()
        if len(data) == 2:
            return data[1]
        else:
            return ""
