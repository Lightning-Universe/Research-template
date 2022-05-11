import logging

from lightning import LightningWork

from research_app.serve import gradio_app

logger = logging.getLogger(__name__)


class GradioWork(LightningWork):
    """
    :param port: Port address for app. By default it will automatically select
    from an internal PORT POOL
    :param blocking: Whether the Work is blocking
    """  # E501

    def __init__(
        self,
        port: int,
        blocking: bool = False,
    ):
        super().__init__(port=port, blocking=blocking)

    def run(self, **interface_kwargs):
        gradio_app.iface.launch(server_port=self.port, **interface_kwargs)
        gradio_app.iface.close()
