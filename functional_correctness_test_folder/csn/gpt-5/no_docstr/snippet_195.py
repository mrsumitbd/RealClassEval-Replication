class KEY_DERIVATION_STRING_DATA_MechanismBase:

    def __init__(self, data, mechType):
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, (bytearray, memoryview)):
            data = bytes(data)
        elif not isinstance(data, (bytes,)):
            raise TypeError(
                "data must be bytes, bytearray, memoryview, or str")
        self._data = data
        self._mech_type = int(mechType)

    def to_native(self):
        return {
            'mechanism': self._mech_type,
            'parameter': self._data,
            'parameter_len': len(self._data),
        }
