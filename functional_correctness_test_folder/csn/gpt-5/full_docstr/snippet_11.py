import pyaes


class AESModeCTR:
    '''Wrapper around pyaes.AESModeOfOperationCTR mode with custom IV'''

    def __init__(self, key, iv):
        '''
        Initializes the AES CTR mode with the given key/iv pair.
        :param key: the key to be used as bytes.
        :param iv: the bytes initialization vector. Must have a length of 16.
        '''
        if not isinstance(key, (bytes, bytearray, memoryview)):
            raise TypeError("key must be bytes-like")
        if not isinstance(iv, (bytes, bytearray, memoryview)):
            raise TypeError("iv must be bytes-like")
        key = bytes(key)
        iv = bytes(iv)
        if len(iv) != 16:
            raise ValueError("iv must be 16 bytes long")
        if len(key) not in (16, 24, 32):
            raise ValueError("key must be 16, 24, or 32 bytes long")
        self.key = key
        self.iv = iv

    def _new_cipher(self):
        counter = pyaes.Counter(int.from_bytes(self.iv, byteorder="big"))
        return pyaes.AESModeOfOperationCTR(self.key, counter=counter)

    def encrypt(self, data):
        '''
        Encrypts the given plain text through AES CTR.
        :param data: the plain text to be encrypted.
        :return: the encrypted cipher text.
        '''
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        cipher = self._new_cipher()
        return cipher.encrypt(bytes(data))

    def decrypt(self, data):
        '''
        Decrypts the given cipher text through AES CTR
        :param data: the cipher text to be decrypted.
        :return: the decrypted plain text.
        '''
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        cipher = self._new_cipher()
        return cipher.decrypt(bytes(data))
