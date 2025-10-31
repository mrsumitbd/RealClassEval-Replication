
import pyaes


class AESModeCTR:
    '''Wrapper around pyaes.AESModeOfOperationCTR mode with custom IV'''

    def __init__(self, key, iv):
        '''
        Initializes the AES CTR mode with the given key/iv pair.
        :param key: the key to be used as bytes.
        :param iv: the bytes initialization vector. Must have a length of 16.
        '''
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes long")
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))
        return aes.encrypt(data)

    def decrypt(self, data):
        '''
        Decrypts the given cipher text through AES CTR
        :param data: the cipher text to be decrypted.
        :return: the decrypted plain text.
        '''
        aes = pyaes.AESModeOfOperationCTR(self.key, pyaes.Counter(self.iv))
        return aes.decrypt(data)
