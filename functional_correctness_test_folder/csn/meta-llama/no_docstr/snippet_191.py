
class AES_GCM_Mechanism:

    def __init__(self, iv, aad, tagBits):
        self.iv = iv
        self.aad = aad
        self.tagBits = tagBits

    def to_native(self):
        return {
            'mechanism': 'CKM_AES_GCM',
            'parameter': {
                'iv': self.iv,
                'aad': self.aad,
                'tagBits': self.tagBits
            }
        }
