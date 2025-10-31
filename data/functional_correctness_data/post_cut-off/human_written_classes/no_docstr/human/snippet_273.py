from loguru import logger
import os

class _TensorboardAdapter:

    def __init__(self):
        import os
        from torch.utils.tensorboard import SummaryWriter
        tensorboard_dir = os.environ.get('TENSORBOARD_DIR', 'tensorboard_log')
        os.makedirs(tensorboard_dir, exist_ok=True)
        logger.info(f'Saving tensorboard log to {tensorboard_dir}.')
        self.writer = SummaryWriter(tensorboard_dir)

    def log(self, data, step):
        for key in data:
            self.writer.add_scalar(key, data[key], step)

    def finish(self):
        self.writer.close()