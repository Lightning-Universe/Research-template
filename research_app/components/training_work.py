import logging
import os
import sys
import warnings
from functools import partial
from typing import Optional

from lightning.components.python import TracerPythonScript

sys.path.insert(0, os.path.dirname(__file__))

logger = logging.getLogger(__name__)


class PLTrainerScript(TracerPythonScript):
    """
    :param flash: Whether the model is lightning-Flash model
    """

    # ref: https://github.com/PyTorchLightning/lightning-quick-start/blob/main/quick_start/components.py#L24
    def __init__(
        self,
        flash: bool = False,
        *args,
        **kwargs,
    ):

        super().__init__(
            *args,
            raise_exception=True,
            **kwargs,
        )
        self.flash = flash
        self.best_model_path = None
        self.run_url = ""
        self.completed = False

    def configure_tracer(self):
        if self.flash:
            from flash import Trainer
        else:
            from pytorch_lightning import Trainer
        from pytorch_lightning.callbacks import Callback
        from pytorch_lightning.loggers import WandbLogger

        tracer = super().configure_tracer()

        class CollectWandbURL(Callback):
            def __init__(self, work):
                self._work = work

            def on_train_start(self, trainer, *_):
                self._work.run_url = trainer.logger.experiment._settings.run_url

        def trainer_pre_fn(self, *args, work=None, **kwargs):
            kwargs["callbacks"] = [CollectWandbURL(work)]
            kwargs["logger"] = [WandbLogger(save_dir=os.path.dirname(__file__))]
            return {}, args, kwargs

        tracer = super().configure_tracer()
        tracer.add_traced(
            Trainer, "__init__", pre_fn=partial(trainer_pre_fn, work=self)
        )
        return tracer

    def run(self, *args, **kwargs):
        warnings.simplefilter("ignore")
        logger.info(f"Running train_script: {self.script_path}")
        super().run(*args, **kwargs)
        self.completed = True
