class KEY_DERIVATION_STRING_DATA_MechanismBase:
    '''Base class for mechanisms using derivation string data'''

    def __init__(self, data, mechType):
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, memoryview):
            data = data.tobytes()
        elif isinstance(data, bytearray):
            data = bytes(data)
        elif not isinstance(data, bytes):
            raise TypeError(
                "data must be bytes, bytearray, memoryview, or str")

        self._data = data
        self._mech_type = mechType

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'mech_type': self._mech_type,
            'pData': self._data,
            'ulLen': len(self._data),
        }
