
class KEY_DERIVATION_STRING_DATA_MechanismBase:
    '''Base class for mechanisms using derivation string data'''

    def __init__(self, data, mechType):
        '''
        :param data: a byte array to concatenate the key with
        :param mechType: mechanism type
        '''
        self.data = data
        self.mechType = mechType

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'data': self.data,
            'mechType': self.mechType
        }
