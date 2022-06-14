import logging
import os
import subprocess
import tempfile
from pathlib import Path

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)


def notebook_to_html(path: str) -> str:
    """Provided notebook file path will be converted into html."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Can't convert notebook to html, path={path} not found!")

    tempdir = tempfile.mkdtemp()
    command = f"jupyter nbconvert --to html {path} --output-dir='{tempdir}' --output index.html"
    subprocess.run(command, shell=True)
    return tempdir


def clone_repo(url: str) -> str:
    """Clones the github repo from url to current dir.

    Example:
        url = "https://github.com/PyTorchLightning/lightning-template-research-app.git"
        clone_repo(url)

    The given repo will be cloned to current dir.
    """
    logger.info(f"cloning {url}")
    tempdir = Path(tempfile.mkdtemp())
    target_path = str(tempdir / os.path.basename(url)).replace(".git", "")
    cmd = f"git clone {url} {target_path}"
    subprocess.run(cmd, shell=True)
    return target_path


if __name__ == "__main__":
    clone_repo("https://github.com/PyTorchLightning/lightning-template-research-app.git")  # E501
