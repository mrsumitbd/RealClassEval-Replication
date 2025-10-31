
class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an integer")
        if not (0 < counterBits <= 128):
            raise ValueError("counterBits must be between 1 and 128")
        if not (isinstance(counterBlock, (bytes, bytearray)) and len(counterBlock) == 16):
            raise ValueError(
                "counterBlock must be a 16-byte bytes or bytearray object")
        self.counterBits = counterBits
        self.counterBlock = bytes(counterBlock)

    def to_native(self):
        # Returns a dict representing the native structure
        return {
            'ulCounterBits': self.counterBits,
            'cb': self.counterBlock
        }
