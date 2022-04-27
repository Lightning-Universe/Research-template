import logging

from lightning import LightningWork
from mkposters import mkposter

from research_app.utils import get_random_port

logger = logging.getLogger(__name__)


class PosterWork(LightningWork):
    """
    :param port: Port address for app.
    :param blocking: Whether the Work is blocking
    """

    def __init__(
        self,
        port=8000,
        code_style="github",
        background_color="#F6F6EF",
        blocking=False,
    ):
        port = port or get_random_port()
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
