import PyKCS11.LowLevel

class AES_CTR_Mechanism:
    """CKM_AES_CTR encryption mechanism"""

    def __init__(self, counterBits, counterBlock):
        """
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        """
        self._param = PyKCS11.LowLevel.CK_AES_CTR_PARAMS()
        self._source_cb = ckbytelist(counterBlock)
        self._param.ulCounterBits = counterBits
        self._param.cb = self._source_cb
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = CKM_AES_CTR
        self._mech.pParameter = self._param
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_AES_CTR_PARAMS_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech