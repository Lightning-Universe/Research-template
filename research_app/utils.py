import os
import socket
import subprocess
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


def get_random_port() -> int:
    # ref: https://stackoverflow.com/questions/1365265/on-localhost-how-do-i-pick-a-free-port-number  E501
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def run_command(cmd):
    """Runs the command with Subprocess module."""
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


def clone_repo(url: str):
    """Clones the github repo from url to current dir."""
    path = Path.cwd() / "github"
    os.makedirs(path, exist_ok=True)
    target_path = str(path / os.path.basename(url)).replace(".git", "")

    if os.path.exists(target_path):
        cmd = f"cd {target_path} && git pull"
    else:
        cmd = f"git clone {url} {target_path}"
    return run_command(cmd)


if __name__ == "__main__":
    clone_repo(
        "https://github.com/PyTorchLightning/lightning-template-research-app.git"  # E501
    )
