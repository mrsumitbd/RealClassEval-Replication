
import ctypes
from ctypes import c_ulong, c_void_p, sizeof


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
        self.mechanism = c_ulong(mechanism)
        if param is None:
            self.parameter = None
            self.size = 0
        else:
            if isinstance(param, (list, tuple)):
                param = bytes(bytearray(param))
            self.parameter = ctypes.create_string_buffer(param)
            self.size = len(param)

    def to_native(self):
        '''convert mechanism to native format'''
        native = ctypes.create_string_buffer(
            ctypes.sizeof(c_ulong) + self.size)
        ctypes.memmove(native, ctypes.addressof(
            self.mechanism), ctypes.sizeof(c_ulong))
        if self.size > 0:
            ctypes.memmove(ctypes.addressof(native) + ctypes.sizeof(c_ulong),
                           ctypes.addressof(self.parameter), self.size)
        return (ctypes.cast(native, c_void_p).value,
                ctypes.sizeof(c_ulong) + self.size)
