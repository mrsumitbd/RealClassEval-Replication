
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os


class AES_GCM_Mechanism:

    def __init__(self, iv, aad, tagBits):
        self.iv = iv
        self.aad = aad
        self.tagBits = tagBits
        # Example key generation, in practice, use a secure method to obtain the key
        self.key = os.urandom(32)
        self.cipher = AESGCM(self.key)

    def to_native(self):
        return {
            'iv': self.iv,
            'aad': self.aad,
            'tagBits': self.tagBits,
            'key': self.key
        }
