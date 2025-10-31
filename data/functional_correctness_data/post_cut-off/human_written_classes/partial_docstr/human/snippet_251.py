import torch

class NVTXRangeContext:
    """
    Context manager which inserts NVTX range around the current context and optionally calls torch.cuda.synchronize
    at the start and the end of the context.

    Args:
        name (str): Name of the NVTX range.
        enabled (bool): Whether the context manager is enabled. When disabled, it does nothing. Default: True.
        synchronize (bool): Whether to call torch.cuda.synchronize() at the start and the end of the context. Default: True.
    """

    def __init__(self, name: str, enabled: bool=True, synchronize: bool=True):
        self.name = name
        self.enabled = enabled
        self.synchronize = synchronize

    def __enter__(self):
        if not self.enabled:
            return
        if self.synchronize:
            torch.cuda.synchronize()
        torch.cuda.nvtx.range_push(self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.enabled:
            return
        if self.synchronize:
            torch.cuda.synchronize()
        torch.cuda.nvtx.range_pop()