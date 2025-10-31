class AES_GCM_Mechanism:
    def __init__(self, iv, aad, tagBits):
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes")
        if not isinstance(aad, (bytes, bytearray)):
            raise TypeError("aad must be bytes")
        if not isinstance(tagBits, int):
            raise TypeError("tagBits must be an integer")
        self.iv = bytes(iv)
        self.aad = bytes(aad)
        self.tagBits = tagBits

    def to_native(self):
        return {
            'iv': self.iv,
            'aad': self.aad,
            'tagBits': self.tagBits
        }
