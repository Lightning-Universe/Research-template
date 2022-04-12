from typing import Dict, List

from app.jupyter import JupyterWork
from lightning import LightningApp, LightningFlow


class Flow(LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.jupyter = JupyterWork()

    def run(self) -> None:
        self.jupyter.run()

    def configure_layout(self) -> List[Dict]:
        return [
            {"name": "Jupyter", "content": self.jupyter.exposed_url("jupyter")},
        ]


app = LightningApp(Flow())
