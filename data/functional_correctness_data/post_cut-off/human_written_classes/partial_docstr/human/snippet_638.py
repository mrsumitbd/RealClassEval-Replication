import torch
from typing import Any, Callable, Dict, Optional, Union
from iree.runtime import BufferUsage, ExternalTimepointFlags, HalBufferView, HalDevice, HalDriver, HalExternalTimepoint, MemoryType, SemaphoreCompatibility, VmInstance, VmModule, create_hal_module, get_driver
from functools import lru_cache

class DeviceState:
    """State for an instantiated HAL device.

    Note that the IREE runtime internally manages a global cache of drivers for
    standard named-access (not custom-constructed) drivers.
    """
    __slots__ = ['device', 'driver', 'instance', 'enumerated_info', 'torch_device', 'torch_stream', 'dlpack_device_type_code']

    def __init__(self, *, driver: Union[str, HalDriver], device: Optional[HalDevice]=None, vm_instance: Optional[VmInstance]=None, enumerated_info: Optional[dict]=None, torch_device: Optional[torch.device]=None, torch_stream: Optional[int]=None, dlpack_device_type_code: int=0):
        self.instance = vm_instance or get_vm_instance()
        self.driver = driver if isinstance(driver, HalDriver) else get_driver(driver)
        self.device = device if device else self.driver.create_default_device()
        self.enumerated_info = enumerated_info or {}
        self.torch_device = torch_device
        self.torch_stream = torch_stream
        self.dlpack_device_type_code = dlpack_device_type_code

    @property
    def enumerated_device_id(self) -> int:
        try:
            return self.enumerated_info['device_id']
        except KeyError as e:
            raise RuntimeError('No enumerated device_id for device') from e

    @property
    def enumerated_path(self) -> str:
        try:
            return self.enumerated_info['path']
        except KeyError as e:
            raise RuntimeError('No enumerated path for device') from e

    @property
    def enumerated_name(self) -> str:
        try:
            return self.enumerated_info['name']
        except KeyError as e:
            raise RuntimeError('No enumerated name for device') from e

    @staticmethod
    @lru_cache(maxsize=None)
    def from_uri(uri: str) -> 'DeviceState':
        driver = get_driver(uri)
        return DeviceState(driver=driver, device=driver.create_device_by_uri(uri))