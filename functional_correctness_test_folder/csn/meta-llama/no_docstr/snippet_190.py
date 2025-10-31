
class AES_CTR_Mechanism:

    def __init__(self, counterBits, counterBlock):
        """
        Initializes an AES_CTR_Mechanism object.

        :param counterBits: The number of bits in the counter block that are used for the counter.
        :param counterBlock: The initial counter block.
        """
        if not isinstance(counterBits, int) or counterBits <= 0:
            raise ValueError("counterBits must be a positive integer")
        if not isinstance(counterBlock, bytes):
            raise ValueError("counterBlock must be bytes")

        self.counterBits = counterBits
        self.counterBlock = counterBlock

    def to_native(self):
        """
        Converts the AES_CTR_Mechanism object to a native representation.

        :return: A dictionary representing the AES_CTR_Mechanism object.
        """
        return {
            'mechanism': 'CKM_AES_CTR',
            'params': {
                'ulCounterBits': self.counterBits,
                'pCounterBlock': self.counterBlock.hex()
            }
        }
