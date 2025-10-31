
class AES_CTR_Mechanism:
    def __init__(self, counterBits, counterBlock):
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an integer")
        if not isinstance(counterBlock, (bytes, bytearray)):
            raise TypeError("counterBlock must be bytes or bytearray")
        self.counterBits = counterBits
        self.counterBlock = bytes(counterBlock)

    def to_native(self):
        return {
            'counterBits': self.counterBits,
            'counterBlock': self.counterBlock
        }
