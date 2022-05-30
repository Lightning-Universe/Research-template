import logging
from typing import Any, Optional

import gradio as gr
from lightning.components.serve import ServeGradio

from ..utils import import_fn_by_name

logger = logging.getLogger(__name__)


class ModelDemo(ServeGradio):
    """Serve model with Gradio UI.

    You need to create a predict.py module with build_model and predict function.
    """

    inputs = gr.inputs.Textbox(default="Doctor Strange Multiverse", label="Search your favourite movie here")
    outputs = gr.outputs.HTML(label="Fetch Images from <b>themoviedb.org</b>")

    # examples = [["A cat reading a book"]]

    def __init__(
        self,
        build_fn: str,
        predict_fn: str,
        parallel: bool = True,
        resource_path: Optional[str] = None,
    ):
        super(ServeGradio, self).__init__(parallel=parallel)
        self._build_fn = import_fn_by_name(build_fn, resource_path)
        self._predict_fn = import_fn_by_name(predict_fn, resource_path)
        self._model = None
        self.ready = False

    def build_model(self) -> Any:
        result = self._build_fn()
        self.ready = True
        return result

    def predict(self, *args, **kwargs):
        return self._predict_fn(self.model, *args, **kwargs)
