import PyKCS11.LowLevel

class KEY_DERIVATION_STRING_DATA_MechanismBase:
    """Base class for mechanisms using derivation string data"""

    def __init__(self, data, mechType):
        """
        :param data: a byte array to concatenate the key with
        :param mechType: mechanism type
        """
        self._param = PyKCS11.LowLevel.CK_KEY_DERIVATION_STRING_DATA()
        self._data = ckbytelist(data)
        self._param.pData = self._data
        self._param.ulLen = len(self._data)
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = mechType
        self._mech.pParameter = self._param
        self._mech.ulParameterLen = PyKCS11.LowLevel.CK_KEY_DERIVATION_STRING_DATA_LENGTH

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech