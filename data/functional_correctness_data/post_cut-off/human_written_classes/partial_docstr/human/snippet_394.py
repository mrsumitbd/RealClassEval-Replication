from src.device_clone.constants import BAR_SIZE_CONSTANTS, BAR_TYPE_MEMORY_64BIT, DEFAULT_CLASS_CODE, DEFAULT_EXT_CFG_CAP_PTR, DEFAULT_REVISION_ID, DEVICE_ID_FALLBACK, MAX_32BIT_VALUE, PCI_CLASS_AUDIO, PCI_CLASS_DISPLAY, PCI_CLASS_NETWORK, PCI_CLASS_STORAGE, POWER_STATE_D0
from src.device_clone.identifier_normalizer import IdentifierNormalizer
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, TypedDict, Union, cast
from src.exceptions import ContextError
from dataclasses import asdict, dataclass, field, fields

@dataclass(slots=True)
class DeviceIdentifiers:
    """Device identification data (uses centralized normalization)."""
    vendor_id: str
    device_id: str
    class_code: str
    revision_id: str
    subsystem_vendor_id: Optional[str] = None
    subsystem_device_id: Optional[str] = None

    def __post_init__(self):
        try:
            norm = IdentifierNormalizer.validate_all_identifiers({'vendor_id': self.vendor_id, 'device_id': self.device_id, 'class_code': self.class_code, 'revision_id': self.revision_id, 'subsystem_vendor_id': self.subsystem_vendor_id, 'subsystem_device_id': self.subsystem_device_id})
        except ContextError as e:
            raise ContextError(str(e))
        self.vendor_id = norm['vendor_id']
        self.device_id = norm['device_id']
        self.class_code = norm['class_code']
        self.revision_id = norm['revision_id']
        self.subsystem_vendor_id = norm['subsystem_vendor_id']
        self.subsystem_device_id = norm['subsystem_device_id']

    @property
    def device_signature(self) -> str:
        return f'{self.vendor_id}:{self.device_id}'

    @property
    def full_signature(self) -> str:
        subsys_vendor = self.subsystem_vendor_id or self.vendor_id
        subsys_device = self.subsystem_device_id or self.device_id
        return f'{self.vendor_id}:{self.device_id}:{subsys_vendor}:{subsys_device}'

    def get_device_class_type(self) -> str:
        class_map = {PCI_CLASS_NETWORK: 'Network Controller', PCI_CLASS_STORAGE: 'Storage Controller', PCI_CLASS_DISPLAY: 'Display Controller', PCI_CLASS_AUDIO: 'Audio Controller'}
        return class_map.get(self.class_code[:2], 'Unknown Device')