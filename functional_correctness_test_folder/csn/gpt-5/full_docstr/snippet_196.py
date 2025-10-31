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
            raise TypeError("mechanism must be an integer")
        self.mechanism = mechanism
        self.param = self._normalize_param(param)

    def _normalize_param(self, param):
        if param is None:
            return None

        # bytes-like directly
        if isinstance(param, (bytes, bytearray, memoryview)):
            return bytes(param)

        # string -> encode as utf-8
        if isinstance(param, str):
            return param.encode('utf-8')

        # list/tuple handling
        if isinstance(param, (list, tuple)):
            # If elements are bytes-like, join
            if all(isinstance(x, (bytes, bytearray, memoryview)) for x in param):
                return b"".join(bytes(x) for x in param)
            # If elements are ints (0-255), make bytes
            if all(isinstance(x, int) for x in param):
                return bytes(param)
            raise TypeError(
                "param list/tuple must contain bytes-like objects or ints")

        # Iterable of ints (not list/tuple), attempt to convert
        try:
            from collections.abc import Iterable
            if isinstance(param, Iterable):
                # Try to convert to bytes; will raise if not ints 0-255
                return bytes(param)
        except Exception:
            pass

        raise TypeError("Unsupported param type")

    def to_native(self):
        '''convert mechanism to native format'''
        if self.param is None:
            return (self.mechanism, None, 0)
        return (self.mechanism, self.param, len(self.param))
