
class CONCATENATE_BASE_AND_KEY_Mechanism:

    def __init__(self, encKey):
        '''
        :param encKey: a handle of encryption key
        '''
        self.encKey = encKey

    def to_native(self):
        '''convert mechanism to native format'''
        # Assuming the native format is a string concatenation of a base string and the encryption key
        base_string = "BASE_STRING_"
        return base_string + str(self.encKey)
