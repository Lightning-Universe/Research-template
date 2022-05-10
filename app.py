from typing import Dict, List, Optional

from lightning import LightningApp, LightningFlow

from research_app.components.gradio_work import GradioWork
from research_app.components.jupyter_work import JupyterWork
from research_app.components.poster_work import PosterWork


class ResearchAppFlow(LightningFlow):
    """
    :param paper: Paper PDF url
    :param blog: Blog web url
    :param github: GitHub repo Url. Repo will be cloned into
    the current directory
    :param experiment_manager: Link for experiment manager like wandb/tensorboard
    :param gradio_port: Gradio will be launched on the provided port.
    By default, it will automatically
    select from a pool of ports
    :param use_jupyter: Whether to launch a Jupyter Notebook
    """

    def __init__(
        self,
        paper: Optional[str] = None,
        blog: Optional[str] = None,
        github: Optional[str] = None,
        experiment_manager: Optional[str] = None,
        poster_port: int = 8000,
        jupyter_port: Optional[int] = None,
        gradio_port: Optional[int] = None,
        use_jupyter: bool = False,
    ) -> None:

        super().__init__()
        self.paper = paper
        self.blog = blog
        self.github = github
        self.use_jupyter = jupyter_port is not None
        self.experiment_manager = experiment_manager
        self.jupyter = None
        self.gradio = GradioWork(port=gradio_port, blocking=False)
        self.poster = PosterWork(port=poster_port, blocking=False)
        if self.use_jupyter:
            self.jupyter = JupyterWork(
                port=jupyter_port, github_url=self.github, blocking=False
            )

    def run(self) -> None:
        if self.use_jupyter:
            self.jupyter.run()
        self.gradio.run()
        self.poster.run()

    def configure_layout(self) -> List[Dict]:
        tabs = []
        tabs.append(
            {
                "name": "Poster",
                "content": self.poster.exposed_url("poster") + "/poster.html",
            }
        )
        if self.paper:
            tabs.append({"name": "Paper", "content": self.paper})
        if self.blog:
            tabs.append({"name": "Blog", "content": self.blog})

        if self.experiment_manager:
            tabs.append(
                {"name": "Experiment Manager", "content": self.experiment_manager}
            )
        if self.use_jupyter:
            tabs.append(
                {
                    "name": "Jupyter",
                    "content": self.jupyter.exposed_url("jupyter"),
                },  # E501
            )
        if self.github:
            tabs.append(
                {"name": "Code", "content": f"https://github.dev/#{self.github}"}
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
    wandb = "https://wandb.ai/aniketmaurya/herbarium-2022/runs/2dvwrme5"

    app = LightningApp(
        ResearchAppFlow(
            paper=paper,
            blog=blog,
            experiment_manager=wandb,
            # jupyter_port=8888,
            gradio_port=8889,
        )
    )
