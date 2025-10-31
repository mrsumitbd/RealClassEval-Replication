
import ctypes
from ctypes import c_ulong, c_char_p, byref, create_string_buffer


class RSA_PSS_Mechanism:
    def __init__(self, mecha, hashAlg, mgf, sLen):
        self.mechanism = mecha
        self.mechanism.pParameter = self._create_parameter(hashAlg, mgf, sLen)

    def to_native(self):
        return self.mechanism

    def _create_parameter(self, hashAlg, mgf, sLen):
        class CK_RSA_PKCS_PSS_PARAMS(ctypes.Structure):
            _fields_ = [
                ("hashAlg", c_ulong),
                ("mgf", c_ulong),
                ("sLen", c_ulong)
            ]

        param = CK_RSA_PKCS_PSS_PARAMS()
        param.hashAlg = hashAlg
        param.mgf = mgf
        param.sLen = sLen

        param_ptr = ctypes.pointer(param)
        return ctypes.cast(param_ptr, c_void_p)

    @property
    def mechanism(self):
        return self._mechanism

    @mechanism.setter
    def mechanism(self, mecha):
        from ctypes import c_ulong, c_void_p

        class CK_MECHANISM(ctypes.Structure):
            _fields_ = [
                ("mechanism", c_ulong),
                ("pParameter", c_void_p),
                ("ulParameterLen", c_ulong)
            ]
        self._mechanism = CK_MECHANISM()
        self._mechanism.mechanism = mecha
        self._mechanism.ulParameterLen = ctypes.sizeof(CK_RSA_PKCS_PSS_PARAMS)
