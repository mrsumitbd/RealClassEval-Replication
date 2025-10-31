
class AES_CTR_Mechanism:
    '''CKM_AES_CTR encryption mechanism'''

    def __init__(self, counterBits, counterBlock):
        """
        :param counterBits: the number of incremented bits in the counter block
        :param counterBlock: a 16-byte initial value of the counter block
        """
        # Validate counterBits
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an integer")
        if counterBits <= 0 or counterBits > 128:
            raise ValueError("counterBits must be between 1 and 128")
        self.counterBits = counterBits

        # Validate counterBlock
        if not isinstance(counterBlock, (bytes, bytearray)):
            raise TypeError("counterBlock must be bytes or bytearray")
        if len(counterBlock) != 16:
            raise ValueError("counterBlock must be exactly 16 bytes long")
        self.counterBlock = bytes(counterBlock)

    def to_native(self):
        """convert mechanism to native format"""
        # In PKCS#11 the native representation is a CK_AES_CTR_PARAMS struct.
        # Here we return a dictionary that mimics that structure.
        return {
            'counterBits': self.counterBits,
            'counterBlock': self.counterBlock,
            'counterBlockLen': len(self.counterBlock)
        }

    def __repr__(self):
        return (f"{self.__class__.__name__}(counterBits={self.counterBits}, "
                f"counterBlock={self.counterBlock.hex()})")
