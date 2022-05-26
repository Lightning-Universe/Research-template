import os
from typing import Dict, List, Optional

from lightning import LightningApp, LightningFlow

from research_app.components.gradio_work import GradioWork
from research_app.components.jupyter_work import JupyterNotebookWork
from research_app.components.poster_work import PosterWork
from research_app.components.work_manager_flow import ManagedWork, WorkManagerFlow


class ResearchApp(LightningFlow):
    """Share everything about your research within a single app.

    :param paper: Paper PDF url
    :param blog: Blog web url
    :param github: GitHub repo Url. Repo will be cloned into
    the current directory
    :param experiment_manager: Link for experiment manager like wandb/tensorboard
    :param enable_notebook: To launch a Jupyter notebook set this to True
    :param enable_gradio: To launch a Gradio notebook set this to True.
    You should update the `research_app/serve/gradio_app.py` file to your use case.
    """

    def __init__(
        self,
        resource_path: str,
        paper: Optional[str] = None,
        blog: Optional[str] = None,
        github: Optional[str] = None,
        experiment_manager: Optional[str] = None,
        enable_notebook: bool = False,
        enable_gradio: bool = False,
    ) -> None:

        super().__init__()
        print("⚡ Lightning Research App! ⚡")
        self.resource_path = os.path.abspath(resource_path)
        self.paper = paper
        self.blog = blog
        self.github = github
        self.experiment_manager = experiment_manager

        works = [
            ManagedWork(
                work=PosterWork(parallel=True, resource_path=self.resource_path),
                name="poster",
                extra_url="/poster.html",
            )
        ]
        if enable_notebook:
            works.append(
                ManagedWork(
                    work=JupyterNotebookWork(github_url=self.github, parallel=True),
                    name="notebook",
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
                        parallel=True,
                        resource_path=self.resource_path,
                    ),
                    name="demo",
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
    paper = "https://arxiv.org/pdf/2103.00020"
    blog = "https://openai.com/blog/clip/"
    github = "https://github.com/openai/CLIP"
    wandb = "https://wandb.ai/cceyda/flax-clip/runs/wlad2c2p?workspace=user-aniketmaurya"

    app = LightningApp(
        ResearchApp(
            resource_path=resource_path,
            paper=paper,
            blog=blog,
            experiment_manager=wandb,
            enable_notebook=True,
            enable_gradio=True,
        )
    )
