
class AES_GCM_Mechanism:
    '''CKM_AES_GCM warpping mechanism'''

    def __init__(self, iv, aad, tagBits):
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes or bytearray")
        if not isinstance(aad, (bytes, bytearray)):
            raise TypeError("aad must be bytes or bytearray")
        if not isinstance(tagBits, int):
            raise TypeError("tagBits must be int")
        if tagBits % 8 != 0 or tagBits < 8 or tagBits > 128:
            raise ValueError(
                "tagBits must be a multiple of 8 between 8 and 128")
        self.iv = bytes(iv)
        self.aad = bytes(aad)
        self.tagBits = tagBits

    def to_native(self):
        return {
            'iv': self.iv,
            'ivLen': len(self.iv),
            'aad': self.aad,
            'aadLen': len(self.aad),
            'tagBits': self.tagBits
        }
