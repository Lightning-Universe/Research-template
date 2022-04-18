import logging

import gradio as gr

logger = logging.getLogger(__name__)


def predict(name):
    return (
        "Hello "
        + name
        + "!! Replace `predict` func with prediction function for your model."
    )


iface = gr.Interface(
    fn=predict,
    inputs="text",
    outputs="text",
)
