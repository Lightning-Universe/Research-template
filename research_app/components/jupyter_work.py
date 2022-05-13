import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

from lightning import LightningWork

from research_app.utils import clone_repo

logger = logging.getLogger(__name__)


class JupyterWork(LightningWork):
    def __init__(
        self,
        github_url: Optional[str] = None,
        blocking=False,
    ):
        super().__init__(blocking=blocking)
        self._proc = None
        self.pid = None
        self.exit_code = None
        self.github_url = github_url
        self.ready = False

    def run(self):
        if self.github_url:
            clone_repo(self.github_url)

        jupyter_notebook_config_path = Path.home() / ".jupyter/jupyter_notebook_config.py"

        try:
            os.remove(jupyter_notebook_config_path)
        except FileNotFoundError:
            logger.debug("Jupyter config didn't exist!")

        cmd = "jupyter notebook --generate-config"

        with subprocess.Popen(
            cmd.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            close_fds=True,
        ) as proc:
            self._proc = proc
            self.pid = proc.pid
            if proc.stdout:
                with proc.stdout:
                    for line in iter(proc.stdout.readline, b""):
                        logger.info("%s", line.decode().rstrip())

            self.exit_code = proc.wait()
            if self.exit_code != 0:
                raise Exception(self.exit_code)

        with open(jupyter_notebook_config_path, "a") as f:
            f.write(
                "c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "
                "\"frame-ancestors * 'self' http://0.0.0.0\","
                ' "Access-Control-Allow-Origin": "http://0.0.0.0"}}'
            )

        cmd = f"jupyter-lab --allow-root --no-browser --ip={self.host} --port={self.port} --NotebookApp.token='' --NotebookApp.password=''"  # noqa: E501

        with subprocess.Popen(
            cmd.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            close_fds=True,
        ) as proc:
            self.ready = True
            self._proc = proc
            self.pid = proc.pid
            if proc.stdout:
                with proc.stdout:
                    for line in iter(proc.stdout.readline, b""):
                        logger.info("%s", line.decode().rstrip())

            self.exit_code = proc.wait()
            if self.exit_code != 0:
                raise Exception(self.exit_code)
