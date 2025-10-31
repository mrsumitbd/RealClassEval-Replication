
from Crypto.Cipher import AES
from Crypto.Util import Counter


class AESModeCTR:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.ctr = Counter.new(
            128, initial_value=int.from_bytes(iv, byteorder='big'))
        self.cipher = AES.new(self.key, AES.MODE_CTR, counter=self.ctr)

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)
