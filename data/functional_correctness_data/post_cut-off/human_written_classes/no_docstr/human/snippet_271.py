from loguru import logger

class LocalLogger:

    def __init__(self, remote_logger=None, enable_wandb=False, print_to_console=False):
        self.print_to_console = print_to_console

    def flush(self):
        pass

    def log(self, data, step):
        if self.print_to_console:
            logger.info(concat_dict_to_str(data, step=step))