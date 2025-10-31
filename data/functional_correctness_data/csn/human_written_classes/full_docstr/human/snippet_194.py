import PyKCS11.LowLevel

class EXTRACT_KEY_FROM_KEY_Mechanism:
    """CKM_EXTRACT_KEY_FROM_KEY key derivation mechanism"""

    def __init__(self, extractParams):
        """
        :param extractParams: the index of the first bit of the original
        key to be used in the newly-derived key.  For example if
        extractParams=5 then the 5 first bits are skipped and not used.
        """
        self._param = PyKCS11.LowLevel.CK_EXTRACT_PARAMS()
        self._param.assign(extractParams)
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = CKM_EXTRACT_KEY_FROM_KEY
        self._mech.pParameter = self._param
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_EXTRACT_PARAMS_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech