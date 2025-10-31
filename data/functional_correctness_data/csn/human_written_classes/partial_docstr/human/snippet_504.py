from random import randint

class I2C:
    """Custom I2C Class for a Generic Agnostic Board"""

    def __init__(self, *, frequency=100000):
        self.freq = frequency

    @staticmethod
    def scan():
        """Mocks an I2C scan and returns a list of 3 randomly generated
        I2C addresses from 0x0 to 0x79.
        """
        address_list = []
        for _ in range(3):
            address_list.append(randint(0, 121))
        return address_list