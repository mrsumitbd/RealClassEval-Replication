
from ctypes import c_ulong, Structure


class CK_MECHANISM(Structure):
    _fields_ = [
        ("mechanism", c_ulong),
        ("pParameter", c_void_p),
        ("ulParameterLen", c_ulong)
    ]


class CK_RSA_PKCS_PSS_PARAMS(Structure):
    _fields_ = [
        ("hashAlg", c_ulong),
        ("mgf", c_ulong),
        ("sLen", c_ulong)
    ]


class RSA_PSS_Mechanism:
    '''RSA PSS Wrapping mechanism'''

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
        '''convert mechanism to native format'''
        mech = CK_MECHANISM()
        mech.mechanism = self.mecha
        mech.pParameter = ctypes.addressof(self.params)
        mech.ulParameterLen = ctypes.sizeof(self.params)
        return mech
