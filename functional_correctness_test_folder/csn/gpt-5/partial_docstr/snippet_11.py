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
        iv_bytes = bytes(iv)
        if len(iv_bytes) != 16:
            raise ValueError("iv must be 16 bytes long")
        self._key = bytes(key)
        self._iv_bytes = iv_bytes
        self._ctr_initial = int.from_bytes(
            self._iv_bytes, byteorder="big", signed=False)

    def _new_ctr_cipher(self):
        counter = pyaes.Counter(self._ctr_initial)  # big-endian by default
        return pyaes.AESModeOfOperationCTR(self._key, counter=counter)

    def encrypt(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        cipher = self._new_ctr_cipher()
        return cipher.encrypt(bytes(data))

    def decrypt(self, data):
        '''
        Decrypts the given cipher text through AES CTR
        :param data: the cipher text to be decrypted.
        :return: the decrypted plain text.
        '''
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        cipher = self._new_ctr_cipher()
        return cipher.decrypt(bytes(data))
