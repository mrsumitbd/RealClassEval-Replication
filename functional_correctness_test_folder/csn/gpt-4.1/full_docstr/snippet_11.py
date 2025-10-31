
import pyaes


class AESModeCTR:
    '''Wrapper around pyaes.AESModeOfOperationCTR mode with custom IV'''

    def __init__(self, key, iv):
        '''
        Initializes the AES CTR mode with the given key/iv pair.
        :param key: the key to be used as bytes.
        :param iv: the bytes initialization vector. Must have a length of 16.
        '''
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes or bytearray")
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes or bytearray")
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes long")
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        '''
        Encrypts the given plain text through AES CTR.
        :param data: the plain text to be encrypted.
        :return: the encrypted cipher text.
        '''
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")
        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(
            int.from_bytes(self.iv, byteorder='big')))
        return aes.encrypt(data)

    def decrypt(self, data):
        '''
        Decrypts the given cipher text through AES CTR
        :param data: the cipher text to be decrypted.
        :return: the decrypted plain text.
        '''
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")
        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(
            int.from_bytes(self.iv, byteorder='big')))
        return aes.decrypt(data)
