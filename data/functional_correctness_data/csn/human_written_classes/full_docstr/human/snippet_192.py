import PyKCS11.LowLevel

class CONCATENATE_BASE_AND_KEY_Mechanism:
    """CKM_CONCATENATE_BASE_AND_KEY key derivation mechanism"""

    def __init__(self, encKey):
        """
        :param encKey: a handle of encryption key
        """
        self._encKey = encKey
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = CKM_CONCATENATE_BASE_AND_KEY
        self._mech.pParameter = self._encKey
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_OBJECT_HANDLE_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech