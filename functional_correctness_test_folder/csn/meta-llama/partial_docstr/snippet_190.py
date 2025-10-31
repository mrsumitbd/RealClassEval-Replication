
from ctypes import c_ulong, Structure, sizeof


class CK_AES_CTR_PARAMS(Structure):
    """CK_AES_CTR_PARAMS is a structure that provides the parameters to the CKM_AES_CTR mechanism."""
    _fields_ = [
        ("ulCounterBits", c_ulong),
        ("cb", c_ulong * 16)  # counter block is 16 bytes
    ]


class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        if len(counterBlock) != 16:
            raise ValueError("Counter block must be 16 bytes")
        if counterBits < 0 or counterBits > 128:
            raise ValueError("Counter bits must be between 0 and 128")

        self.params = CK_AES_CTR_PARAMS()
        self.params.ulCounterBits = counterBits
        for i, byte in enumerate(counterBlock):
            self.params.cb[i] = byte

    def to_native(self):
        return self.params
