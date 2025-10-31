
import ctypes
from ctypes import c_ulong, c_ubyte, Structure


class CK_AES_CTR_PARAMS(Structure):
    _fields_ = [
        ("ulCounterBits", c_ulong),
        ("cb", c_ubyte * 16)
    ]


class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        '''
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        '''
        if len(counterBlock) != 16:
            raise ValueError("Counter block must be 16 bytes long")
        if counterBits < 0 or counterBits > 128:
            raise ValueError("Counter bits must be between 0 and 128")

        self.counterBits = counterBits
        self.counterBlock = counterBlock

    def to_native(self):
        '''convert mechanism to native format'''
        params = CK_AES_CTR_PARAMS()
        params.ulCounterBits = self.counterBits
        for i in range(16):
            params.cb[i] = self.counterBlock[i]

        mechanism = (c_ulong * 3)()
        mechanism[0] = 0x00001082  # CKM_AES_CTR
        mechanism[1] = ctypes.addressof(params)
        mechanism[2] = ctypes.sizeof(params)

        return ctypes.cast(mechanism, ctypes.POINTER(c_ulong))


# Example usage:
if __name__ == "__main__":
    counterBlock = b'\x00' * 16
    mechanism = AES_CTR_Mechanism(128, counterBlock)
    native_mechanism = mechanism.to_native()
