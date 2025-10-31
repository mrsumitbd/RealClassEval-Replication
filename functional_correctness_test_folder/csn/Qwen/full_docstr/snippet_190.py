
import struct


class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        if not isinstance(counterBits, int) or not (0 <= counterBits <= 128):
            raise ValueError(
                "counterBits must be an integer between 0 and 128")
        if not isinstance(counterBlock, bytes) or len(counterBlock) != 16:
            raise ValueError("counterBlock must be a 16-byte bytes object")

        self.counterBits = counterBits
        self.counterBlock = counterBlock

    def to_native(self):
        '''convert mechanism to native format'''
        # Assuming native format is a byte representation of counterBits and counterBlock
        return struct.pack('>I', self.counterBits) + self.counterBlock
