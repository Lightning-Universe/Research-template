from typing import Dict, List, Optional

from lightning import LightningApp, LightningFlow

from research_app.components.gradio_work import GradioWork
from research_app.components.jupyter_work import JupyterWork
from research_app.components.training_work import PLTrainerScript
from research_app.train.train import train_script_path


class ResearchAppFlow(LightningFlow):
    """
    :param paper: Paper PDF url
    :param blog: Blog web url
    :param github: GitHub repo Url. Repo will be cloned into
    the current directory
    :param jupyter_port: Jupyter will be launched on the provided port.
    By default, it will automatically
    select from a pool of ports
    :param gradio_port: Gradio will be launched on the provided port.
    By default, it will automatically
    select from a pool of ports
    """

    def __init__(
        self,
        paper: Optional[str] = None,
        blog: Optional[str] = None,
        github: Optional[str] = None,
        video: Optional[str] = None,
        jupyter_port=None,
        gradio_port=None,
    ) -> None:

        super().__init__()
        self.paper = paper
        self.blog = blog
        self.github = github
        self.video = video
        self.jupyter = JupyterWork(
            port=jupyter_port, github_url=github, blocking=False
        )  # E501
        # self.gradio = GradioWork(port=gradio_port, blocking=False)
        self.train_script = PLTrainerScript(
            script_path=train_script_path, deployment_port=gradio_port, flash=True
        )

    def run(self) -> None:
        self.jupyter.run()
        self.train_script.run()

    def configure_layout(self) -> List[Dict]:
        tabs = []
        if self.paper:
            tabs.append({"name": "Paper", "content": self.paper})
        if self.blog:
            tabs.append({"name": "Blog", "content": self.blog})
        if self.video:
            tabs.append({"name": "Video", "content": self.video})

        tabs.append(
            {
                "name": "Jupyter",
                "content": self.jupyter.exposed_url("jupyter"),
            },  # E501
        )
        tabs.append(
            {
                "name": "Deployment",
                "content": self.train_script.exposed_url("gradio"),
            },  # E501
        )

        tabs.append({"name": "WandB", "content": self.train_script.run_url})
        return tabs


if __name__ == "__main__":
    paper = "https://arxiv.org/pdf/1811.06965.pdf"
    blog = "https://openai.com/blog/clip/"
    github = "https://github.com/mlfoundations/open_clip"
    video = "https://www.youtube.com/embed/W-O7AZNzbzQ"

    app = LightningApp(
        ResearchAppFlow(
            jupyter_port=8888,
            gradio_port=8889,
            paper=paper,
            blog=blog,
            github=None,
            video=video,
        )
    )
