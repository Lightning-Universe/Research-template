import logging
import os
import subprocess
from pathlib import Path

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)


def notebook_to_html(path: str) -> str:
    """Provided notebook file path will be converted into html."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Can't convert notebook to html, path={path} not found!")

    folder = os.path.dirname(path)
    converted_html = path.replace("ipynb", "html")
    renamed_html = folder + "/index.html"
    if os.path.exists(converted_html) or os.path.exists(renamed_html):
        logger.info(f"Skipping nbconvert, {path} converted into html!")
    else:
        command = f"jupyter nbconvert --to html {path}"
        subprocess.run(command, shell=True)
        os.rename(converted_html, renamed_html)
    return folder


def clone_repo(url: str) -> str:
    """Clones the github repo from url to current dir.

    Example:
        url = "https://github.com/PyTorchLightning/lightning-template-research-app.git"
        clone_repo(url)

    The given repo will be cloned to current dir.
    """
    logger.info(f"cloning {url}")
    path = Path.cwd() / "github"
    os.makedirs(path, exist_ok=True)
    target_path = str(path / os.path.basename(url)).replace(".git", "")

    if os.path.exists(target_path):
        logger.info("Skipped git clone, repo already exists!")
    else:
        cmd = f"git clone {url} {target_path}"
        subprocess.run(cmd, shell=True)
    return target_path


if __name__ == "__main__":
    clone_repo("https://github.com/PyTorchLightning/lightning-template-research-app.git")  # E501
