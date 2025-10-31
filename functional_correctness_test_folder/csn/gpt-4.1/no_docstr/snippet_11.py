
from Crypto.Cipher import AES
from Crypto.Util import Counter


class AESModeCTR:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        ctr = Counter.new(128, initial_value=int.from_bytes(
            self.iv, byteorder='big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.encrypt(data)

    def decrypt(self, data):
        ctr = Counter.new(128, initial_value=int.from_bytes(
            self.iv, byteorder='big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(data)
