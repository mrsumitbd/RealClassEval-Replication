
class CONCATENATE_BASE_AND_KEY_Mechanism:
    '''CKM_CONCATENATE_BASE_AND_KEY key derivation mechanism'''

    def __init__(self, encKey):
        '''
        :param encKey: a handle of encryption key
        '''
        self.encKey = encKey

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'mechanism': 'CKM_CONCATENATE_BASE_AND_KEY',
            'encKey': self.encKey
        }
