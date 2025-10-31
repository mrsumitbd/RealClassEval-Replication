class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an integer")
        if not (1 <= counterBits <= 128):
            raise ValueError("counterBits must be between 1 and 128 inclusive")
        try:
            cb = bytes(counterBlock)
        except Exception as e:
            raise TypeError("counterBlock must be a bytes-like object") from e
        if len(cb) != 16:
            raise ValueError("counterBlock must be exactly 16 bytes")
        self.counterBits = counterBits
        self.counterBlock = cb

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'ulCounterBits': self.counterBits,
            'cb': self.counterBlock,
        }
