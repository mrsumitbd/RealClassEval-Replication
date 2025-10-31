
from Crypto.Cipher import AES
from Crypto.Util import Counter
import struct


class AES_CTR_Mechanism:

    def __init__(self, counterBits, counterBlock):
        self.counter = Counter.new(
            counterBits, initial_value=int.from_bytes(counterBlock, byteorder='big'))
        self.cipher = AES.new(b'\x00' * 16, AES.MODE_CTR, counter=self.counter)

    def to_native(self):
        return self.cipher.encryptor()
