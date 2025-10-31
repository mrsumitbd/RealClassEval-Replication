import torch
import platform
import ctypes
from iree.runtime import BufferUsage, ExternalTimepointFlags, HalBufferView, HalDevice, HalDriver, HalExternalTimepoint, MemoryType, SemaphoreCompatibility, VmInstance, VmModule, create_hal_module, get_driver

class _HipSemaphoreInterop:

    def __init__(self, sync):
        if platform.system() == 'Windows':
            self.library = ctypes.CDLL('amdhip64.dll')
        else:
            self.library = ctypes.CDLL('libamdhip64.so')
        self.library.hipEventCreate.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int32]
        self.library.hipEventCreate.restype = ctypes.c_int32
        self.library.hipEventRecord.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.library.hipEventRecord.restype = ctypes.c_int32
        self.library.hipEventDestroy.argtypes = [ctypes.c_void_p]
        self.library.hipEventDestroy.restype = ctypes.c_int32
        self.library.hipStreamWaitEvent.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.library.hipStreamWaitEvent.restype = ctypes.c_int32
        self.library.hipEventQuery.argtypes = [ctypes.c_void_p]
        self.library.hipEventQuery.restype = ctypes.c_int32
        self.sync = sync

    def get_timepoint_import(self):
        if not self.sync:
            return None
        evt = ctypes.c_void_p(0)
        ret = self.library.hipEventCreate(evt, 2)
        if ret != 0:
            raise RuntimeError('Could not create hip event')
        ret = self.library.hipEventRecord(evt, ctypes.c_void_p(torch.cuda.current_stream().cuda_stream))
        if ret != 0:
            raise RuntimeError('Could not record hip event')
        timepoint = HalExternalTimepoint()
        timepoint.compatibility = SemaphoreCompatibility.DEVICE_WAIT
        timepoint.flags = ExternalTimepointFlags.NONE
        timepoint.hip_event = evt.value
        return timepoint

    def wait_exported_timepoint(self, timepoint: HalExternalTimepoint):
        if not self.sync:
            return
        ret = self.library.hipStreamWaitEvent(ctypes.c_void_p(torch.cuda.current_stream().cuda_stream), ctypes.c_void_p(timepoint.hip_event), 0)
        if ret != 0:
            raise RuntimeError('Could not wait on event')

    def destroy_timepoint_event(self, timepoint: HalExternalTimepoint):
        if not self.sync:
            return True
        ret = self.library.hipEventDestroy(ctypes.c_void_p(timepoint.hip_event))
        if ret != 0:
            raise RuntimeError(f'Could not destroy event got {ret}')
        return True