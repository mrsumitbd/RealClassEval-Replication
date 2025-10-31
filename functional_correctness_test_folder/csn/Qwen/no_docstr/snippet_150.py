
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad
import os


class MaltegoOauth:

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        with open(private_key_path, 'rb') as key_file:
            private_key = RSA.import_key(key_file.read(), passphrase=password)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        return cipher_rsa.decrypt(ciphertext)

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        iv = ciphertext[:AES.block_size]
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher_aes.decrypt(ciphertext[AES.block_size:]), AES.block_size)

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        decoded_ciphertext = base64.b64decode(encoded_ciphertext)
        rsa_encrypted_key = decoded_ciphertext[:256]
        aes_encrypted_data = decoded_ciphertext[256:]
        aes_key = cls._rsa_decrypt(private_key_path, rsa_encrypted_key)
        return cls._aes_decrypt(aes_key, aes_encrypted_data)
