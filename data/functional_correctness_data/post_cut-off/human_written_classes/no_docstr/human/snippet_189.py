from pytorch_fob.engine.parameter_groups import GroupedModel
from lightning.pytorch.utilities.types import OptimizerLRScheduler
from pytorch_fob.engine.configs import OptimizerConfig

class Optimizer:

    def __init__(self, config: OptimizerConfig) -> None:
        self.config = config

    def configure_optimizers(self, model: GroupedModel) -> OptimizerLRScheduler:
        optimizer_module = import_optimizer(self.config.name)
        return optimizer_module.configure_optimizers(model, self.config)