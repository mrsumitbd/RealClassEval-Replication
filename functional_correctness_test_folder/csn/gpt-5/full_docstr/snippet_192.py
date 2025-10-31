class CONCATENATE_BASE_AND_KEY_Mechanism:
    '''CKM_CONCATENATE_BASE_AND_KEY key derivation mechanism'''

    def __init__(self, encKey):
        '''
        :param encKey: a handle of encryption key
        '''
        if isinstance(encKey, bool) or not isinstance(encKey, int):
            raise TypeError("encKey must be an integer handle")
        if encKey < 0:
            raise ValueError("encKey must be non-negative")
        self.encKey = encKey

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            "mechanism": "CKM_CONCATENATE_BASE_AND_KEY",
            "parameter": self.encKey,
        }
