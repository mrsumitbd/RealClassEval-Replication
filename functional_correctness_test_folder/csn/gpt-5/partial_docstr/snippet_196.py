class Mechanism:
    '''Wraps CK_MECHANISM'''

    def __init__(self, mechanism, param=None):
        self.mechanism = mechanism
        self.param = self._normalize_param(param)

    def _normalize_param(self, param):
        if param is None:
            return None
        if isinstance(param, (bytes, bytearray, memoryview)):
            return bytes(param)
        if isinstance(param, str):
            return param.encode('utf-8')
        if isinstance(param, int):
            if param == 0:
                return b'\x00'
            length = (param.bit_length() + 7) // 8
            return param.to_bytes(length, byteorder='big')
        try:
            # Try buffer protocol
            return bytes(param)
        except Exception as e:
            raise TypeError(
                f"Unsupported parameter type: {type(param).__name__}") from e

    def to_native(self):
        '''convert mechanism to native format'''
        if self.param is None:
            return {
                'mechanism': self.mechanism,
                'parameter': None,
                'parameter_len': 0
            }
        return {
            'mechanism': self.mechanism,
            'parameter': self.param,
            'parameter_len': len(self.param)
        }
