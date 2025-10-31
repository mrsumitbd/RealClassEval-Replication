
class AES_GCM_Mechanism:
    '''CKM_AES_GCM wrapping mechanism'''

    def __init__(self, iv, aad, tagBits):
        self.iv = iv
        self.aad = aad
        self.tagBits = tagBits

    def to_native(self):
        return {
            'iv': self.iv,
            'aad': self.aad,
            'tagBits': self.tagBits
        }
