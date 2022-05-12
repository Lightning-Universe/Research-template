import logging
from typing import Any, Optional

from lightning.components.serve import ServeGradio

from ..utils import import_fn_by_name

logger = logging.getLogger(__name__)


class GradioWork(ServeGradio):
    """
    :param port: Port address for app. By default it will automatically select
    from an internal PORT POOL
    :param blocking: Whether the Work is blocking
    """  # E501

    def __init__(
        self,
        inputs: Any,
        outputs: Any,
        build_fn: str,
        predict_fn: str,
        blocking: bool = False,
        resource_path: Optional[str] = None,
    ):
        super(ServeGradio, self).__init__(blocking=blocking)
        self.inputs = inputs
        self.outputs = outputs
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
