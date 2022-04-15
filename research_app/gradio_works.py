import logging
from typing import Callable

import gradio as gr
from lightning import LightningWork

logger = logging.getLogger(__name__)


def predict(name):
    return (
        "Hello "
        + name
        + "!! Replace `predict` func with prediction function for your model."
    )


class GradioWork(LightningWork):
    def __init__(
        self,
        host="0.0.0.0",
        port=8889,
    ):
        super().__init__(exposed_ports={"gradio": port}, blocking=False)
        self.host = host
        self.port = port

    def run(
        self,
        gradio_fn: Callable = predict,
        inputs="text",
        outputs="text",
        **interface_kwargs
    ):
        iface = gr.Interface(
            fn=gradio_fn, inputs=inputs, outputs=outputs, **interface_kwargs
        )
        iface.launch(server_port=self.port)
