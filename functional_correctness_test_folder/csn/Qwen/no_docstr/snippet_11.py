
from Crypto.Cipher import AES
from Crypto.Util import Counter


class AESModeCTR:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.block_size = AES.block_size
        self.counter = Counter.new(
            128, initial_value=int.from_bytes(iv, byteorder='big'))

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CTR, counter=self.counter)
        return cipher.encrypt(data)

    def decrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CTR, counter=self.counter)
        return cipher.decrypt(data)
