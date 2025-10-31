class KEY_DERIVATION_STRING_DATA_MechanismBase:
    '''Base class for mechanisms using derivation string data'''

    def __init__(self, data, mechType):
        '''
        :param data: a byte array to concatenate the key with
        :param mechType: mechanism type
        '''
        if not isinstance(mechType, int):
            raise TypeError("mechType must be an int")
        if data is None:
            raise ValueError("data must not be None")
        if isinstance(data, str):
            raise TypeError("data must be bytes-like, not str")
        try:
            data_bytes = bytes(data)
        except Exception as e:
            raise TypeError("data must be bytes-like") from e

        self.data = data_bytes
        self.mechType = mechType
        self.length = len(self.data)

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'mech_type': self.mechType,
            'parameter': self.data,
            'length': self.length,
        }
