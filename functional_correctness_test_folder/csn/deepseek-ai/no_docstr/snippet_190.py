
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class AES_CTR_Mechanism:

    def __init__(self, counterBits, counterBlock):
        self.counterBits = counterBits
        self.counterBlock = counterBlock
        self.key = os.urandom(32)  # 256-bit key for AES-256
        self.nonce = os.urandom(16)  # 16-byte nonce for CTR mode

    def to_native(self):
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CTR(self.nonce),
            backend=default_backend()
        )
        return cipher
