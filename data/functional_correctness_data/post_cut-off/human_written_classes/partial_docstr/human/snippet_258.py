import torch

class add_nvtx_event:
    """
    Context manager to add an NVTX event around a code block.

    Args:
        event_name (str): The name of the event to be recorded.
    """

    def __init__(self, event_name: str):
        self.enter_name = event_name

    def __enter__(self):
        if torch.compiler.is_compiling():
            nvtx_range_push('torch compile region')
        else:
            torch.cuda.nvtx.range_push(self.enter_name)
        return self

    def __exit__(self, *excinfo):
        if torch.compiler.is_compiling():
            nvtx_range_pop()
        else:
            torch.cuda.nvtx.range_pop()