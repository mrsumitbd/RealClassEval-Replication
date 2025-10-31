
from ctypes import c_ulong, Structure, c_void_p


class CK_RSA_PKCS_PSS_PARAMS(Structure):
    _fields_ = [
        ("hashAlg", c_ulong),
        ("mgf", c_ulong),
        ("sLen", c_ulong)
    ]


class RSA_PSS_Mechanism:

    def __init__(self, mecha, hashAlg, mgf, sLen):
        '''
        :param mecha: the mechanism to use (like
          `CKM_SHA384_RSA_PKCS_PSS`)
        :param hashAlg: the hash algorithm to use (like `CKM_SHA384`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA384`)
        :param sLen: length, in bytes, of the salt value used in the PSS
          encoding (like 0 or the message length)
        '''
        self.mecha = mecha
        self.params = CK_RSA_PKCS_PSS_PARAMS(hashAlg, mgf, sLen)

    def to_native(self):
        return (self.mecha, c_void_p(ctypes.addressof(self.params)), ctypes.sizeof(self.params))
