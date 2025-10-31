import PyKCS11.LowLevel

class AES_GCM_Mechanism:
    """CKM_AES_GCM warpping mechanism"""

    def __init__(self, iv, aad, tagBits):
        """
        :param iv: initialization vector
        :param aad: additional authentication data
        :param tagBits: length of authentication tag in bits
        """
        self._param = PyKCS11.LowLevel.CK_GCM_PARAMS()
        self._source_iv = ckbytelist(iv)
        self._param.pIv = self._source_iv
        self._param.ulIvLen = len(self._source_iv)
        self._source_aad = ckbytelist(aad)
        self._param.pAAD = self._source_aad
        self._param.ulAADLen = len(self._source_aad)
        self._param.ulTagBits = tagBits
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = CKM_AES_GCM
        self._mech.pParameter = self._param
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_GCM_PARAMS_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech