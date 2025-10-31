
import ctypes
from ctypes import c_void_p, c_ulong


class Mechanism:
    '''Wraps CK_MECHANISM'''

    def __init__(self, mechanism, param=None):
        self.mechanism = c_ulong(mechanism)
        if param is None:
            self.param = c_void_p(None)
            self.param_size = c_ulong(0)
        else:
            self.param = c_void_p(ctypes.addressof(param))
            self.param_size = c_ulong(ctypes.sizeof(param))

    def to_native(self):
        '''convert mechanism to native format'''
        class CK_MECHANISM(ctypes.Structure):
            _fields_ = [
                ("mechanism", c_ulong),
                ("pParameter", c_void_p),
                ("ulParameterLen", c_ulong)
            ]
        return CK_MECHANISM(self.mechanism, self.param, self.param_size)
