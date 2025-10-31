from iree.runtime import BufferUsage, ExternalTimepointFlags, HalBufferView, HalDevice, HalDriver, HalExternalTimepoint, MemoryType, SemaphoreCompatibility, VmInstance, VmModule, create_hal_module, get_driver

class _NullSemaphoreInterop:

    def __init__(self, sync):
        self.sync = sync

    def get_timepoint_import(self):
        return None

    def wait_exported_timepoint(self, timepoint: HalExternalTimepoint):
        pass

    def destroy_timepoint_event(self, timepoint: HalExternalTimepoint):
        return True