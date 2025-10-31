
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os


class AES_GCM_Mechanism:
    '''CKM_AES_GCM wrapping mechanism'''

    def __init__(self, iv, aad, tagBits):
        '''
        :param iv: initialization vector
        :param aad: additional authentication data
        :param tagBits: length of authentication tag in bits
        '''
        self.iv = iv
        self.aad = aad
        self.tagBits = tagBits
        # Example key generation, in practice, manage keys securely
        self.key = os.urandom(32)
        self.cipher = AESGCM(self.key)

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'iv': self.iv,
            'aad': self.aad,
            'tagBits': self.tagBits,
            'key': self.key
        }

    def encrypt(self, plaintext):
        '''Encrypts the plaintext using AES-GCM'''
        return self.cipher.encrypt(self.iv, plaintext, self.aad)

    def decrypt(self, ciphertext):
        '''Decrypts the ciphertext using AES-GCM'''
        return self.cipher.decrypt(self.iv, ciphertext, self.aad)
