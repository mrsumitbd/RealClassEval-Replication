class CONCATENATE_BASE_AND_KEY_Mechanism:
    def __init__(self, encKey):
        """
        :param encKey: a handle of encryption key
        """
        self.encKey = encKey

    def to_native(self):
        """convert mechanism to native format"""
        return {
            'mechanism': 'CONCATENATE_BASE_AND_KEY',
            'key': self.encKey
        }
