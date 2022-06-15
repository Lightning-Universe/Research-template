import logging
import os
import subprocess
from pathlib import Path

import lightning as L

logger = logging.getLogger(__name__)


class JupyterLab(L.LightningWork):
    def __init__(self):
        super().__init__(parallel=True)

    def run(self):
        jupyter_notebook_config_path = Path.home() / ".jupyter/jupyter_notebook_config.py"
        try:
            os.remove(jupyter_notebook_config_path)
        except FileNotFoundError:
            logger.debug("Jupyter config didn't exist!")

        cmd = "jupyter notebook --generate-config"
        subprocess.run(cmd, shell=True)

        with open(jupyter_notebook_config_path, "a") as f:
            f.write(
                "c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "
                "\"frame-ancestors * 'self' http://0.0.0.0\","
                ' "Access-Control-Allow-Origin": "http://0.0.0.0"}}'
            )

        cmd = f"jupyter-lab --allow-root --no-browser --ip={self.host} --port={self.port} --NotebookApp.token='' --NotebookApp.password=''"  # noqa: E501
        subprocess.run(cmd, shell=True)
