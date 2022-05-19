import os
from typing import Dict, List, Optional

from lightning import LightningApp, LightningFlow

from research_app.components.gradio_work import GradioWork
from research_app.components.jupyter_work import JupyterWork
from research_app.components.poster_work import PosterWork
from research_app.components.work_manager_flow import ManagedWork, WorkManagerFlow


class ResearchAppFlow(LightningFlow):
    """
    :param paper: Paper PDF url
    :param blog: Blog web url
    :param github: GitHub repo Url. Repo will be cloned into
    the current directory
    :param experiment_manager: Link for experiment manager like wandb/tensorboard
    :param enable_jupyter: To launch a Jupyter notebook set this to True
    :param enable_gradio: To launch a Gradio notebook set this to True.
    You should update the `research_app/serve/gradio_app.py` file to your use case.
    :param jupyter_port: Provide a port to launch Jupyter
    :param gradio_port: Gradio will be launched on the provided port.
    """

    def __init__(
        self,
        resource_path: str,
        paper: Optional[str] = None,
        blog: Optional[str] = None,
        github: Optional[str] = None,
        experiment_manager: Optional[str] = None,
        enable_jupyter: bool = False,
        enable_gradio: bool = False,
    ) -> None:

        super().__init__()
        self.resource_path = os.path.abspath(resource_path)
        self.paper = paper
        self.blog = blog
        self.github = github
        self.experiment_manager = experiment_manager

        works = [
            ManagedWork(
                work=PosterWork(parallel=False, resource_path=self.resource_path),
                name="poster",
                extra_url="/poster.html",
            )
        ]
        if enable_jupyter:
            works.append(
                ManagedWork(
                    work=JupyterWork(github_url=self.github, parallel=False),
                    name="jupyter",
                )
            )
        if enable_gradio:
            works.append(
                ManagedWork(
                    work=GradioWork(
                        "image",
                        "text",
                        "predict.build_model",
                        "predict.predict",
                        parallel=False,
                        resource_path=self.resource_path,
                    ),
                    name="predict",
                )
            )

        self.work_manager = WorkManagerFlow(*works)

    def run(self) -> None:
        self.work_manager.run()

    def configure_layout(self) -> List[Dict]:
        tabs = []

        if self.paper:
            tabs.append({"name": "Paper", "content": self.paper})
        if self.blog:
            tabs.append({"name": "Blog", "content": self.blog})

        if self.experiment_manager:
            tabs.append({"name": "Experiment Manager", "content": self.experiment_manager})
        if self.github:
            tabs.append({"name": "Code", "content": f"https://github.dev/#{self.github}"})

        if not self.work_manager.all_ready:
            tabs.append({"name": "Waiting room", "content": self.work_manager})

        for work in ManagedWork.get_all_from_instance(self.work_manager):
            if work.work.ready:
                tabs.append({"name": work.name, "content": work.work.url + work.extra_url})

        return tabs


if __name__ == "__main__":
    resource_path = "resources"
    paper = "https://arxiv.org/pdf/2103.00020.pdf"
    blog = "https://openai.com/blog/clip/"
    github = "https://github.com/mlfoundations/open_clip"
    wandb = "https://wandb.ai/aniketmaurya/herbarium-2022/runs/2dvwrme5"

    app = LightningApp(
        ResearchAppFlow(
            resource_path=resource_path,
            paper=paper,
            blog=blog,
            experiment_manager=wandb,
            enable_jupyter=True,
            enable_gradio=True,
        )
    )
