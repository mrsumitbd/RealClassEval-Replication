import PyKCS11.LowLevel

class Mechanism:
    """Wraps CK_MECHANISM"""

    def __init__(self, mechanism, param=None):
        """
        :param mechanism: the mechanism to be used
        :type mechanism: integer, any `CKM_*` value
        :param param: data to be used as crypto operation parameter
          (i.e. the IV for some algorithms)
        :type param: string or list/tuple of bytes

        :see: :func:`Session.decrypt`, :func:`Session.sign`
        """
        self._mech = PyKCS11.LowLevel.CK_MECHANISM()
        self._mech.mechanism = mechanism
        self._param = None
        if param:
            self._param = ckbytelist(param)
            self._mech.pParameter = self._param
            self._mech.ulParameterLen = len(param)

    def to_native(self):
        """convert mechanism to native format"""
        return self._mech