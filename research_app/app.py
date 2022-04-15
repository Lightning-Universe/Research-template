from typing import Dict, List, Optional

from gradio_works import GradioWork
from jupyter_works import JupyterWork
from lightning import LightningApp, LightningFlow


class ResearchAppFlow(LightningFlow):
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
        self.jupyter = JupyterWork(port=jupyter_port, blocking=False)
        self.gradio = GradioWork(port=gradio_port, blocking=False)

    def run(self) -> None:
        self.jupyter.run()
        self.gradio.run()

    def configure_layout(self) -> List[Dict]:
        tabs = []
        if self.paper:
            tabs.append({"name": "Paper", "content": self.paper})
        if self.blog:
            tabs.append({"name": "Blog", "content": self.blog})

        tabs.append(
            {
                "name": "Jupyter",
                "content": self.jupyter.exposed_url("jupyter"),
            },  # E501
        )
        tabs.append(
            {
                "name": "Deployment",
                "content": self.gradio.exposed_url("gradio"),
            },  # E501
        )
        return tabs


if __name__ == "__main__":
    paper = "https://arxiv.org/pdf/1811.06965.pdf"
    blog = "https://openai.com/blog/clip/"
    github = "https://github.com/mlfoundations/open_clip"

    app = LightningApp(ResearchAppFlow(paper=paper, blog=blog, github=github))
