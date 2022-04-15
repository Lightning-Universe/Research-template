import os
import subprocess
from logging import getLogger
from pathlib import Path
from typing import Optional

from lightning import LightningWork

logger = getLogger(__name__)


def run_command(cmd):
    with subprocess.Popen(
        cmd.split(" "),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
        close_fds=True,
    ) as proc:
        if proc.stdout:
            with proc.stdout:
                for line in iter(proc.stdout.readline, b""):
                    logger.info("%s", line.decode().rstrip())

        exit_code = proc.wait()
        if exit_code != 0:
            raise Exception(exit_code)
        return exit_code


def clone_repo(url):
    path = Path.cwd() / "github"
    os.makedirs(path, exist_ok=True)
    target_path = str(path / os.path.basename(url))[:-4]

    if os.path.exists(target_path):
        cmd = f"cd {target_path} && git pull"
    else:
        cmd = f"git clone {url} {target_path}"
    return run_command(cmd)


class UtilityWork(LightningWork):
    def __init__(self, github_url: Optional[str] = None, blocking=False):
        super().__init__(blocking=blocking)
        self.github_url = github_url
        self.exit_code = None

    def run(self):
        if self.github_url:
            self.exit_code = clone_repo(self.github_url)


if __name__ == "__main__":
    clone_repo(
        "https://github.com/PyTorchLightning/lightning-template-research-app.git"  # noqa E501
    )
