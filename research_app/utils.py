import os
import subprocess
from logging import getLogger
from pathlib import Path

from rich import print

logger = getLogger(__name__)


def notebook_to_html(path: str):
    command = f"jupyter nbconvert --to html {path}"
    subprocess.run(command, shell=True)
    folder = "/".join(path.split("/")[:-1])
    html = path.replace("ipynb", "html")
    os.rename(html, folder + "/index.html")
    return folder


def clone_repo(url: str):
    """Clones the github repo from url to current dir."""
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
