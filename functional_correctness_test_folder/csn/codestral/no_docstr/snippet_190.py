
class AES_CTR_Mechanism:

    def __init__(self, counterBits, counterBlock):

        self.counterBits = counterBits
        self.counterBlock = counterBlock

    def to_native(self):

        return (self.counterBits, self.counterBlock)
