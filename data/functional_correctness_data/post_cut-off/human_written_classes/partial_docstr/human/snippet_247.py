import os

class Sampler:
    """
    A sampler function for setting the epoch number and iteration number.
    In webdataset, information is propagated using environment flags.
    In our case,
        WDS_EPOCH_NUM: Epoch number
        WDS_START_INDEX: Start index in this epoch.
    """

    def __init__(self, mode: str):
        self.mode = mode
        assert self.mode in ['train', 'val']

    def set_epoch(self, epoch: int):
        if self.mode == 'train':
            os.environ['WDS_EPOCH_NUM'] = str(epoch)
        else:
            pass

    def set_iteration(self, start_index: int):
        if self.mode == 'train':
            os.environ['WDS_START_INDEX'] = str(start_index)
        else:
            pass