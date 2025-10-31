
class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        self.counterBits = counterBits
        self.counterBlock = counterBlock

    def to_native(self):
        return {
            'counterBits': self.counterBits,
            'counterBlock': self.counterBlock
        }
