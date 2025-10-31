
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os


class MaltegoOauth:

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password.encode() if password else None,
                backend=default_backend()
            )
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        ciphertext = base64.b64decode(encoded_ciphertext)
        aes_key_encrypted = cls._rsa_decrypt(
            private_key_path, ciphertext[:256], os.getenv('PRIVATE_KEY_PASSWORD'))
        aes_key = aes_key_encrypted[:32]
        ciphertext = ciphertext[256:]
        return cls._aes_decrypt(aes_key, ciphertext).decode('utf-8')
