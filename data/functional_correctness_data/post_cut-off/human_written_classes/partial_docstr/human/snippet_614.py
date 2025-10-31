from typing import Dict
from dataclasses import dataclass, field

@dataclass
class DeviceIdentificationResponse:
    """Modbus TCP client function read_device_identification() response struct.

    :param conformity_level: this represents supported access and object type
    :type conformity_level: int
    :param more_follows: for stream request can be set to 0xff if other objects are available (0x00 in other cases)
    :type more_follows: int
    :param next_object_id: the next object id to be asked by following transaction
    :type next_object_id: int
    :param objects_by_id: a dictionary with requested object (dict keys are object id as int)
    :type objects_by_id: dict
    """
    conformity_level: int = 0
    more_follows: int = 0
    next_object_id: int = 0
    objects_by_id: Dict[int, bytes] = field(default_factory=lambda: {})

    @property
    def vendor_name(self):
        return self.objects_by_id.get(0)

    @property
    def product_code(self):
        return self.objects_by_id.get(1)

    @property
    def major_minor_revision(self):
        return self.objects_by_id.get(2)

    @property
    def vendor_url(self):
        return self.objects_by_id.get(3)

    @property
    def product_name(self):
        return self.objects_by_id.get(4)

    @property
    def model_name(self):
        return self.objects_by_id.get(5)

    @property
    def user_application_name(self):
        return self.objects_by_id.get(6)