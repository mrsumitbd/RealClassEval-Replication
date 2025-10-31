
import struct


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
        # Assuming to_native should return a byte representation of the mechanism
        # Here we pack the counterBits and counterBlock into a byte structure
        # counterBits is an integer, and counterBlock is a 16-byte block
        return struct.pack('>I16s', self.counterBits, self.counterBlock)
