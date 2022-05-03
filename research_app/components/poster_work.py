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
        port: int,
        code_style="github",
        background_color="#F6F6EF",
        blocking=False,
    ):
        super().__init__(exposed_ports={"poster": port}, blocking=blocking)
        self.port = port
        self.code_style = code_style
        self.background_color = background_color

    def run(self):
        mkposter(
            datadir="research_app/poster",
            background_color=self.background_color,
            code_style=self.code_style,
        )
