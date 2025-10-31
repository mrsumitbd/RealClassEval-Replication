class CONCATENATE_BASE_AND_KEY_Mechanism:

    def __init__(self, encKey):
        '''
        :param encKey: a handle of encryption key
        '''
        if encKey is None:
            raise ValueError("encKey must not be None")
        try:
            self.encKey = int(encKey)
        except (TypeError, ValueError):
            raise TypeError("encKey must be an integer-like handle")
        if self.encKey < 0:
            raise ValueError("encKey must be a non-negative integer handle")

    def to_native(self):
        '''convert mechanism to native format'''
        return self.encKey
