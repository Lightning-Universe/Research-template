import logging
import os
import subprocess
from pathlib import Path

from rich import print
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)


def notebook_to_markdown(path: str):
    """Provided notebook file path will be converted into markdown."""
    command = f"jupyter nbconvert --to markdown {path}"
    subprocess.run(command, shell=True)


def notebook_to_html(path: str):
    """Provided notebook file path will be converted into html."""
    command = f"jupyter nbconvert --to html {path}"
    subprocess.run(command, shell=True)
    folder = "/".join(path.split("/")[:-1])
    html = path.replace("ipynb", "html")
    os.rename(html, folder + "/index.html")
    return folder


def clone_repo(url: str):
    """Clones the github repo from url to current dir.

    Example:
        url = "https://github.com/PyTorchLightning/lightning-template-research-app.git"
        clone_repo(url)

    The given repo will be cloned to current dir.
    """
    print(f"cloning {url}")
    path = Path.cwd() / "github"
    os.makedirs(path, exist_ok=True)
    target_path = str(path / os.path.basename(url)).replace(".git", "")

    if os.path.exists(target_path):
        cmd = f"cd {target_path} && git pull"
    else:
        cmd = f"git clone {url} {target_path}"
    return subprocess.run(cmd, shell=True), target_path


if __name__ == "__main__":
    clone_repo("https://github.com/PyTorchLightning/lightning-template-research-app.git")  # E501
