
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
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.sLen = sLen

    def to_native(self):
        return {
            'mechanism': self.mecha,
            'hashAlg': self.hashAlg,
            'mgf': self.mgf,
            'sLen': self.sLen
        }
