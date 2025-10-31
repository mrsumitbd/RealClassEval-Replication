
import ctypes


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
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.sLen = sLen

    def to_native(self):
        '''convert mechanism to native format'''
        class CK_RSA_PKCS_PSS_PARAMS(ctypes.Structure):
            _fields_ = [
                ("hashAlg", ctypes.c_ulong),
                ("mgf", ctypes.c_ulong),
                ("sLen", ctypes.c_ulong),
            ]

        params = CK_RSA_PKCS_PSS_PARAMS(
            self.hashAlg,
            self.mgf,
            self.sLen,
        )
        # Return a tuple that can be used directly with PyKCS11 or similar
        return (self.mecha, ctypes.byref(params))
