from iree.runtime import BufferUsage, ExternalTimepointFlags, HalBufferView, HalDevice, HalDriver, HalExternalTimepoint, MemoryType, SemaphoreCompatibility, VmInstance, VmModule, create_hal_module, get_driver
import torch

class _CudaSemaphoreInterop:

    def __init__(self, sync):
        self.sync = sync
        pass

    def get_timepoint_import(self):
        torch.cuda.current_stream().synchronize()
        return None

    def wait_exported_timepoint(self, timepoint: HalExternalTimepoint):
        pass

    def destroy_timepoint_event(self, timepoint: HalExternalTimepoint):
        return True