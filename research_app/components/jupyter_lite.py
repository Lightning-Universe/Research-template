import logging
import os.path
import subprocess
from typing import Optional

import lightning as L

logger = logging.getLogger(__name__)


class JupyterLite(L.LightningWork):
    """This component will launch JupyterLab instance that runs entirely in the browser.

    https://jupyterlite.readthedocs.io/en/latest/
    """
# @Aniket describe init param?
    def __init__(self, github_url: Optional[str] = None, contents="research_app", **kwargs):
        super().__init__(parallel=True, **kwargs)
        assert os.path.exists(contents), f"{contents} not exist at {os.getcwd()}"
        self.contents = contents
        self.github_url = github_url
        self.ready = False

    def run(self):
        cmd = "jupyter lite init"
        subprocess.run(cmd, shell=True)

        cmd = "jupyter lite build"
        subprocess.run(cmd, shell=True)

        cmd = f"jupyter lite serve --contents {self.contents} --port {self.port}"
        subprocess.run(cmd, shell=True)
        self.ready = True

# @Aniket do you need this code here?
if __name__ == "__main__":
    from lightning import LightningApp, LightningFlow

    class Demo(LightningFlow):
        def __init__(self) -> None:
            super().__init__()
            self.lite = JupyterLite(github_url="https://github.com/openai/CLIP")

        def run(self):
            self.lite.run()

        def configure_layout(self):
            return [{"name": "lite", "content": self.lite.url}]

    app = LightningApp(Demo())
