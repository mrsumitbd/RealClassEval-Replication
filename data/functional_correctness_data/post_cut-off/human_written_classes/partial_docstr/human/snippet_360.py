from torch import nn

class MemoryBufferModuleWrapper:
    """
    Note that we do not design MemoryBufferModuleWrapper as an nn.Module due to
    - It will change the checkpoint name
    """

    def __init__(self, module: nn.Module):
        super().__init__()
        self.module = module
        self.weight_buffer_meta = get_weight_buffer_meta_from_module(self.module)
        self.memory_buffers = build_memory_buffer(self.weight_buffer_meta)
        build_memory_reference_from_module(self.module, self.memory_buffers)

    def get_memory_buffers(self):
        return self.memory_buffers

    def get_weight_buffer_meta(self):
        return self.weight_buffer_meta