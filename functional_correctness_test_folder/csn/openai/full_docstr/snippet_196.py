
class Mechanism:
    '''Wraps CK_MECHANISM'''

    def __init__(self, mechanism, param=None):
        '''
        :param mechanism: the mechanism to be used
        :type mechanism: integer, any `CKM_*` value
        :param param: data to be used as crypto operation parameter
          (i.e. the IV for some algorithms)
        :type param: string or list/tuple of bytes
        :see: :func:`Session.decrypt`, :func:`Session.sign`
        '''
        if not isinstance(mechanism, int):
            raise TypeError(
                f"mechanism must be an int, got {type(mechanism).__name__}")
        self.mechanism = mechanism

        if param is None:
            self.param = None
        elif isinstance(param, (bytes, bytearray, memoryview)):
            self.param = bytes(param)
        elif isinstance(param, str):
            self.param = param.encode()
        elif isinstance(param, (list, tuple)):
            try:
                self.param = bytes(param)
            except Exception as exc:
                raise TypeError(
                    "param list/tuple must contain integers 0-255") from exc
        else:
            raise TypeError(
                f"param must be None, bytes-like, string, or list/tuple of ints, got {type(param).__name__}")

    def to_native(self):
        '''convert mechanism to native format'''
        # In many PKCS#11 wrappers, a CK_MECHANISM is represented as a tuple
        # (mechanism, parameter).  If no parameter is supplied, the second
        # element is None.
        return (self.mechanism, self.param)
