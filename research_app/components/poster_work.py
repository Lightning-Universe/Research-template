import logging

from lightning import LightningWork
from mkposters import mkposter

logger = logging.getLogger(__name__)


class PosterWork(LightningWork):
    """
    :param port: Port address for app.
    :param blocking: Whether the Work is blocking
    """

    def __init__(
        self,
        resource_path: str,
        code_style="github",
        background_color="#F6F6EF",
        blocking=False,
    ):
        super().__init__(blocking=blocking)
        self.resource_path = resource_path
        self.code_style = code_style
        self.background_color = background_color

    def run(self):
        print(self.resource_path)
        mkposter(
            datadir=self.resource_path,
            background_color=self.background_color,
            code_style=self.code_style,
            port=self.port,
        )
