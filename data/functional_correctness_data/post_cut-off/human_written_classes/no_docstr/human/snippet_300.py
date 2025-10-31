from os import urandom
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class FastEncryptor:

    def __init__(self, key=None):
        self.key = key

    def _get_cipher(self):
        return ChaCha20Poly1305(self.key)

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        nonce = urandom(12)
        cipher = self._get_cipher()
        return nonce + cipher.encrypt(nonce, data, None)

    def decrypt(self, data):
        try:
            nonce = data[:12]
            ciphertext = data[12:]
            cipher = self._get_cipher()
            return cipher.decrypt(nonce, ciphertext, None).decode()
        except Exception as e:
            return None

    def __getstate__(self):
        return {'key': self.key}

    def __setstate__(self, state):
        self.key = state['key']