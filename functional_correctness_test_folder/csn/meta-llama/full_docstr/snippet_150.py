
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json


class MaltegoOauth:
    '''
    A Crypto Helper for Maltego OAuth Secrets received from the Transform Distribution Server
    The TDS will send back an encrypted combination of the following :
    1. Token
    2. Token Secret
    3. Refresh Token
    4. Expires In
    Contains Methods:
        1. decrypt_secrets(private_key_path="pem file", ciphertext="request.getTransformSetting('name from TDS')")
    '''
    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        '''
        RSA Decryption function, returns decrypted plaintext in b64 encoding
        '''
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password,
                backend=default_backend()
            )
        decrypted_key = private_key.decrypt(
            base64.b64decode(ciphertext),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(decrypted_key).decode('utf-8')

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES Decryption function, returns decrypted plaintext value
        '''
        key = base64.b64decode(key)
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(
            ciphertext[16:]) + decryptor.finalize()
        return json.loads(decrypted_data.decode('utf-8'))

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        '''
        The TDS will send back an encrypted combination of the following :
        1. Token
        2. Token Secret
        3. Refresh Token
        4. Expires In
        This function decodes the combinations and decrypts as required and returns a dictionary with the following keys
                {"token":"",
                "token_secret": "",
                "refresh_token": "",
                "expires_in": ""}
        '''
        aes_key = cls._rsa_decrypt(
            private_key_path=private_key_path, ciphertext=encoded_ciphertext)
        decrypted_secrets = cls._aes_decrypt(
            key=aes_key, ciphertext=encoded_ciphertext)
        return decrypted_secrets
