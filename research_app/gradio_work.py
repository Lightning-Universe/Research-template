import logging

import gradio as gr
from lightning import LightningWork
from utils import get_random_port

logger = logging.getLogger(__name__)


class GradioWork(LightningWork):
    """
    :param port: Port address for app. By default it will automatically select
    from an internal PORT POOL
    :param blocking: Whether the Work is blocking
    """

    def __init__(
        self,
        port=None,
        blocking=False,
    ):
        port = port or get_random_port()
        super().__init__(exposed_ports={"gradio": port}, blocking=blocking)
        self.port = port

    def run(self, iface: gr.Interface):
        iface.launch(server_port=self.port)
        iface.close()
