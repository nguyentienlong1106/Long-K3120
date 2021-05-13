import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    if "GIT_DIR" in os.environ:
        gitdir_name = os.environ.get("GIT_DIR", default=".git")
    else:
        gitdir_name = pathlib.Path(".git")
    while os.path.isdir(workdir):
        if os.path.isdir(workdir / pathlib.Path(gitdir_name)):
            return pathlib.Path(workdir) / gitdir_name
        if workdir == ".":
            break
        workdir = pathlib.Path(workdir.parent)
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if os.path.isfile(workdir):
        raise Exception(f"{workdir} is not a directory")
    if "GIT_DIR" in os.environ:
        gitdir_name = workdir / pathlib.Path(os.environ["GIT_DIR"])
    else:
        gitdir_name = workdir / pathlib.Path(".git")
    os.mkdir(gitdir_name)
    os.makedirs(gitdir_name / "refs" / "heads")
    os.mkdir(gitdir_name / "refs" / "tags")
    os.mkdir(gitdir_name / "objects")
    with (gitdir_name / "HEAD").open("w") as head:
        head.write("ref: refs/heads/master\n")
    with (gitdir_name / "config").open("w") as config:
        config.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    with (gitdir_name / "description").open("w") as description:
        description.write("Unnamed pyvcs repository.\n")
    return gitdir_name
