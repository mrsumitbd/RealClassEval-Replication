class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an int")
        if not (1 <= counterBits <= 128):
            raise ValueError("counterBits must be in the range 1..128")

        if isinstance(counterBlock, (bytes, bytearray, memoryview)):
            cb = bytes(counterBlock)
        else:
            raise TypeError("counterBlock must be a bytes-like object")

        if len(cb) != 16:
            raise ValueError("counterBlock must be exactly 16 bytes long")

        self.counterBits = counterBits
        self.counterBlock = cb

    def to_native(self):
        import struct
        return struct.pack("=I16s", self.counterBits, self.counterBlock)
