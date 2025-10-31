class AES_CTR_Mechanism:

    def __init__(self, counterBits, counterBlock):
        if not isinstance(counterBits, int):
            raise TypeError("counterBits must be an integer")
        if counterBits <= 0 or counterBits > 128 or counterBits % 8 != 0:
            raise ValueError(
                "counterBits must be a positive multiple of 8 and no greater than 128")
        if not isinstance(counterBlock, (bytes, bytearray)):
            raise TypeError("counterBlock must be bytes or bytearray")
        if len(counterBlock) != 16:
            raise ValueError("counterBlock must be exactly 16 bytes long")
        self._counter_bits = counterBits
        self._counter_block = bytes(counterBlock)

    def to_native(self):
        return {
            "counterBits": self._counter_bits,
            "counterBlock": self._counter_block,
        }
