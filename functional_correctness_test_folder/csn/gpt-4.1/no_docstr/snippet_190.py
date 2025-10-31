
class AES_CTR_Mechanism:

    def __init__(self, counterBits, counterBlock):
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an integer")
        if not (0 <= counterBits <= 128):
            raise ValueError("counterBits must be between 0 and 128")
        if not isinstance(counterBlock, (bytes, bytearray)):
            raise TypeError("counterBlock must be bytes or bytearray")
        if len(counterBlock) != 16:
            raise ValueError("counterBlock must be 16 bytes long")
        self.counterBits = counterBits
        self.counterBlock = bytes(counterBlock)

    def to_native(self):
        return {
            'counterBits': self.counterBits,
            'counterBlock': self.counterBlock
        }
