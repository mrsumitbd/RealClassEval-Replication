import PyKCS11.LowLevel

class RSA_PSS_Mechanism:
    """RSA PSS Wrapping mechanism"""

    def __init__(self, mecha, hashAlg, mgf, sLen):
        """
        :param mecha: the mechanism to use (like
          `CKM_SHA384_RSA_PKCS_PSS`)
        :param hashAlg: the hash algorithm to use (like `CKM_SHA384`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA384`)
        :param sLen: length, in bytes, of the salt value used in the PSS
          encoding (like 0 or the message length)
        """
        self._param = PyKCS11.LowLevel.CK_RSA_PKCS_PSS_PARAMS()
        self._param.hashAlg = hashAlg
        self._param.mgf = mgf
        self._param.sLen = sLen
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = mecha
        self._mech.pParameter = self._param
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_RSA_PKCS_PSS_PARAMS_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech