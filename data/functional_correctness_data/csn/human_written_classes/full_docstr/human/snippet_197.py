import PyKCS11.LowLevel

class RSAOAEPMechanism:
    """RSA OAEP Wrapping mechanism"""

    def __init__(self, hashAlg, mgf, label=None):
        """
        :param hashAlg: the hash algorithm to use (like `CKM_SHA256`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA256`)
        :param label: the (optional) label to use
        """
        self._param = PyKCS11.LowLevel.CK_RSA_PKCS_OAEP_PARAMS()
        self._param.hashAlg = hashAlg
        self._param.mgf = mgf
        self._source = None
        self._param.source = CKZ_DATA_SPECIFIED
        if label:
            self._source = ckbytelist(label)
            self._param.ulSourceDataLen = len(self._source)
        else:
            self._param.ulSourceDataLen = 0
        self._param.pSourceData = self._source
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = CKM_RSA_PKCS_OAEP
        self._mech.pParameter = self._param
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_RSA_PKCS_OAEP_PARAMS_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech