import logging
import os
from typing import Dict, List, Optional

from lightning import LightningApp, LightningFlow

from research_app.components.jupyter_lite import JupyterLite
from research_app.components.markdown_poster import Poster
from research_app.components.model_demo import ModelDemo

logger = logging.getLogger(__name__)


class ResearchApp(LightningFlow):
    """Share your paper "bundled" with the arxiv link, poster, live jupyter notebook, interactive demo to try the model
    and more!

    :param paper: Paper PDF url
    :param blog: Blog web url
    :param github: GitHub repo Url. Repo will be cloned into
    the current directory
    :param training_log_url: Link for experiment manager like wandb/tensorboard
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
        training_log_url: Optional[str] = None,
        enable_notebook: bool = False,
        enable_gradio: bool = False,
    ) -> None:

        super().__init__()
        self.resource_path = os.path.abspath(resource_path)
        self.paper = paper
        self.blog = blog
        self.github = github
        self.training_logs = training_log_url
        self.enable_notebook = enable_notebook
        self.enable_gradio = enable_gradio
        self.poster = Poster(parallel=True, resource_path=self.resource_path)

        if enable_notebook:
            self.notebook = JupyterLite(self.github)

        if enable_gradio:
            self.model_demo = ModelDemo()

    def run(self) -> None:
        if os.environ.get("TESTING_LAI"):
            print("⚡ Lightning Research App! ⚡")
        self.poster.run()
        if self.enable_notebook:
            self.notebook.run()
        if self.enable_gradio:
            self.model_demo.run()

    def configure_layout(self) -> List[Dict]:
        tabs = []

        if self.blog:
            tabs.append({"name": "Blog", "content": self.blog})

        if self.paper:
            tabs.append({"name": "Paper", "content": self.paper})

        tabs.append({"name": "Poster", "content": self.poster.url + "/poster.html"})

        if self.enable_notebook:
            tabs.append({"name": "Notebook", "content": self.notebook.url})

        if self.training_logs:
            tabs.append({"name": "Training Logs", "content": self.training_logs})

        if self.enable_gradio:
            tabs.append({"name": "Model Demo", "content": self.model_demo.url})

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
            training_log_url=wandb,
            github=github,
            enable_notebook=True,
            enable_gradio=True,
        )
    )
