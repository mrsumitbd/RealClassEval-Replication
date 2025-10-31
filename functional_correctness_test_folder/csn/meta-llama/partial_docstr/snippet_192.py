
import ctypes
from ctypes import c_char_p, c_ulong


class CONCATENATE_BASE_AND_KEY_Mechanism:
    def __init__(self, encKey):
        '''
        :param encKey: a handle of encryption key
        '''
        self.mechanism = ctypes.c_ulong(0)  # assuming mechanism type is ulong
        # assuming parameter is a void pointer
        self.parameter = ctypes.c_void_p(encKey)
        # assuming parameter length is ulong
        self.parameter_len = ctypes.c_ulong(0)

    def to_native(self):
        '''convert mechanism to native format'''
        native_mechanism = ctypes.c_ulong(self.mechanism.value)
        native_parameter = ctypes.cast(self.parameter, c_char_p)
        native_parameter_len = ctypes.c_ulong(ctypes.sizeof(self.parameter))

        class CK_MECHANISM(ctypes.Structure):
            _fields_ = [
                ("mechanism", ctypes.c_ulong),
                ("pParameter", ctypes.c_void_p),
                ("ulParameterLen", ctypes.c_ulong)
            ]

        native_mechanism_struct = CK_MECHANISM()
        native_mechanism_struct.mechanism = native_mechanism
        native_mechanism_struct.pParameter = ctypes.cast(
            native_parameter, ctypes.c_void_p)
        native_mechanism_struct.ulParameterLen = native_parameter_len

        return ctypes.byref(native_mechanism_struct)
