import logging
import os
import subprocess

from lightning import LightningWork

logger = logging.getLogger(__name__)


def notebook_dir_setup(folder_name: str):
    path = f"{os.getcwd()}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    subprocess.run(f"chmod -R 664 {path}", shell=True)


class LitJupyter(LightningWork):
    def __init__(self, notebook_dir="./notebooks", **kwargs):
        super().__init__(parallel=True, **kwargs)
        self.notebook_dir = notebook_dir

    def run(self):
        notebook_dir_setup(self.notebook_dir)
        remove_pwd = "--NotebookApp.token='' --NotebookApp.password=''"
        host_info = f"--ip={self.host} --port={self.port}"
        cmd = f"jupyter-notebook --allow-root --no-browser {host_info} {remove_pwd} --notebook-dir {self.notebook_dir}"
        subprocess.run(cmd, shell=True)
