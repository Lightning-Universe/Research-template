import logging

from lightning import LightningWork
from mkposters import mkposter

logger = logging.getLogger(__name__)


class Poster(LightningWork):
    """This component lets you create a poster using markdown.

    To make a poster you should create a `poster.md` file in the `resource_dir`.

    resource_dir: folder path where poster.md is present.
    code_style: The style of code blocks.
    background_color: The background color of the poster.
    """

    def __init__(
        self,
        resource_dir: str,
        code_style="github",
        background_color="#F6F6EF",
    ):
        super().__init__(parallel=True)
        self.resource_dir = resource_dir
        self.code_style = code_style
        self.background_color = background_color

    def run(self):
        mkposter(
            datadir=self.resource_dir,
            background_color=self.background_color,
            code_style=self.code_style,
            port=self.port,
        )
