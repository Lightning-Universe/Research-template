import logging
import os
import sys
import warnings
from functools import partial

from lightning.components.python import TracerPythonScript

sys.path.insert(0, os.path.dirname(__file__))


logger = logging.getLogger(__name__)


class PLTrainerScript(TracerPythonScript):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, raise_exception=True, **kwargs)
        self.best_model_path = None
        self.run_url = ""

    def configure_tracer(self):
        from flash import Trainer
        from pytorch_lightning.callbacks import Callback
        from pytorch_lightning.loggers import WandbLogger

        class CollectWandbURL(Callback):
            def __init__(self, work):
                self._work = work

            def on_train_start(self, trainer, *_):
                self._work.run_url = trainer.logger.experiment._settings.run_url  # E501

        def trainer_pre_fn(self, *args, **kwargs):
            kwargs["callbacks"] = kwargs.get("callbacks", [])
            kwargs["callbacks"].append(CollectWandbURL(self))
            kwargs["logger"] = [WandbLogger(save_dir=os.path.dirname(__file__))]  # E501
            return {}, args, kwargs

        tracer = super().configure_tracer()
        tracer.add_traced(Trainer, "__init__", pre_fn=partial(trainer_pre_fn))
        return tracer

    def run(self, *args, **kwargs):
        warnings.simplefilter("ignore")
        logger.info(f"Running train_script: {self.script_path}")
        super().run(*args, **kwargs)
