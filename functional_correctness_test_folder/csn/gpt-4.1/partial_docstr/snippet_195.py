
class KEY_DERIVATION_STRING_DATA_MechanismBase:
    '''Base class for mechanisms using derivation string data'''

    def __init__(self, data, mechType):
        self.data = data
        self.mechType = mechType

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'mechanism': self.mechType,
            'parameter': self.data
        }
