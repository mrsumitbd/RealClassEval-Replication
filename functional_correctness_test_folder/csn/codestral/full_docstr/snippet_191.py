
class AES_GCM_Mechanism:
    '''CKM_AES_GCM warpping mechanism'''

    def __init__(self, iv, aad, tagBits):
        '''
        :param iv: initialization vector
        :param aad: additional authentication data
        :param tagBits: length of authentication tag in bits
        '''
        self.iv = iv
        self.aad = aad
        self.tagBits = tagBits

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'iv': self.iv,
            'aad': self.aad,
            'tagBits': self.tagBits
        }
