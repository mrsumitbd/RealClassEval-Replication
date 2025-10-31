
class CK_MECHANISM:
    def __init__(self, mechanism, parameter=None):
        self.mechanism = mechanism
        self.parameter = parameter


class KEY_DERIVATION_STRING_DATA_MechanismBase:
    '''Base class for mechanisms using derivation string data'''

    def __init__(self, data, mechType):
        self.data = data
        self.mechType = mechType

    def to_native(self):
        '''convert mechanism to native format'''
        return CK_MECHANISM(self.mechType, self.data.encode('utf-8'))
