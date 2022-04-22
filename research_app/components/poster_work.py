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
        blocking=False,
    ):
        port = port or get_random_port()
        super().__init__(exposed_ports={"poster": port}, blocking=blocking)
        self.port = port

    def run(self):
        mkposter("research_app/poster")
