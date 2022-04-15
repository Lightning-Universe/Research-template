from typing import Dict, List

from jupyter_works import JupyterWork
from gradio_works import GradioWork
from lightning import LightningApp, LightningFlow


class Flow(LightningFlow):
    def __init__(self, jupyter_port=8888, gradio_port=8889) -> None:
        super().__init__()
        self.jupyter = JupyterWork(port=jupyter_port)
        self.gradio = GradioWork(port=gradio_port)

    def run(self) -> None:
        self.gradio.run()
        self.jupyter.run()

    def configure_layout(self) -> List[Dict]:
        return [
            {"name": "Arxiv", "content": "https://arxiv.org/pdf/1811.06965.pdf"},
            {"name": "Jupyter", "content": self.jupyter.exposed_url("jupyter")},
            {"name": "Deployment", "content": self.gradio.exposed_url("gradio")},
        ]


app = LightningApp(Flow())
