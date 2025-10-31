class AES_GCM_Mechanism:
    '''CKM_AES_GCM warpping mechanism'''

    def __init__(self, iv, aad, tagBits):
        if iv is None:
            raise ValueError("iv must not be None")
        if aad is None:
            aad = b""
        if isinstance(iv, bytearray):
            iv = bytes(iv)
        if isinstance(aad, bytearray):
            aad = bytes(aad)
        if not isinstance(iv, (bytes, memoryview)):
            raise TypeError("iv must be bytes-like")
        if not isinstance(aad, (bytes, memoryview)):
            raise TypeError("aad must be bytes-like")
        if not isinstance(tagBits, int) or tagBits <= 0:
            raise ValueError("tagBits must be a positive integer")
        self.iv = bytes(iv)
        self.aad = bytes(aad)
        self.tagBits = int(tagBits)

    def to_native(self):
        iv_len = len(self.iv)
        aad_len = len(self.aad)
        iv_bits = iv_len * 8
        return (self.iv, iv_len, iv_bits, self.aad, aad_len, self.tagBits)
