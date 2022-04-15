from typing import Dict, List, Optional

from gradio_works import GradioWork
from jupyter_works import JupyterWork
from lightning import LightningApp, LightningFlow


class Flow(LightningFlow):
    def __init__(
            self,
            paper: Optional[str] = None,
            blog: Optional[str] = None,
            github: Optional[str] = None,
            jupyter_port=8888,
            gradio_port=8889,
    ) -> None:
        super().__init__()
        self.paper = paper
        self.blog = blog
        self.github = github
        self.jupyter = JupyterWork(port=jupyter_port)
        # self.gradio = GradioWork(port=gradio_port, blocking=True)

    def run(self) -> None:
        self.jupyter.run()
        # self.gradio.run()

    @property
    def vscode(self):
        return f"https://vscode.dev/{self.github}"

    def configure_layout(self) -> List[Dict]:
        tabs = []
        if self.paper:
            tabs.append({"name": "Paper", "content": self.paper})
        if self.blog:
            tabs.append({"name": "Blog", "content": self.blog})
        if self.github:
            tabs.append({"name": "vscode", "content": self.vscode})
        tabs.append(
            {"name": "Jupyter", "content": self.jupyter.exposed_url("jupyter")},
        )
        return tabs


if __name__ == "__main__":
    paper = "https://arxiv.org/pdf/1811.06965.pdf"
    blog = "https://openai.com/blog/clip/"
    github = "https://github.com/mlfoundations/open_clip"

    app = LightningApp(Flow(paper=paper, blog=blog, github=github))
