from deeppavlov.core.commands.utils import expand_path

class TBWriter:

    def __init__(self, tensorboard_log_dir: str):
        from torch.utils.tensorboard import SummaryWriter
        tensorboard_log_dir = expand_path(tensorboard_log_dir)
        self.tb_train_writer = SummaryWriter(str(tensorboard_log_dir / 'train_log'))
        self.tb_valid_writer = SummaryWriter(str(tensorboard_log_dir / 'valid_log'))

    def write_train(self, tag, scalar_value, global_step):
        self.tb_train_writer.add_scalar(tag, scalar_value, global_step)

    def write_valid(self, tag, scalar_value, global_step):
        self.tb_valid_writer.add_scalar(tag, scalar_value, global_step)

    def flush(self):
        self.tb_train_writer.flush()
        self.tb_valid_writer.flush()