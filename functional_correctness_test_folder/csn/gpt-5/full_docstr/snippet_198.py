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
        if sLen is None:
            raise ValueError("sLen must not be None")
        if isinstance(sLen, bool) or not isinstance(sLen, int):
            raise TypeError("sLen must be an integer")
        if sLen < 0:
            raise ValueError("sLen must be >= 0")

        self.mecha = mecha
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.sLen = sLen

    def to_native(self):
        '''convert mechanism to native format'''
        return (
            self.mecha,
            {
                'hashAlg': self.hashAlg,
                'mgf': self.mgf,
                'sLen': self.sLen,
            }
        )
