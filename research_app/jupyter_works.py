import logging
import os
import subprocess
from pathlib import Path

from lightning import LightningWork

logger = logging.getLogger(__name__)


class JupyterWork(LightningWork):
    def __init__(self, host="0.0.0.0", port=8888):
        super().__init__(exposed_ports={"jupyter": 8888})
        self._proc = None
        self.host = host
        self.port = port
        self.pid = None
        self.exit_code = None

    def run(self):

        jupyter_notebook_config_path = (
            Path.home() / ".jupyter/jupyter_notebook_config.py"
        )

        if os.path.exists(jupyter_notebook_config_path):
            os.remove(jupyter_notebook_config_path)
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
                """c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors * 'self' "}}
                ServerApp.password=lightning
                """  # noqa E501
            )

        cmd = "jupyter lab --ip 0.0.0.0"

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
