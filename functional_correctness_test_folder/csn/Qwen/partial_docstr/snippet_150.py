
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
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
        with open(private_key_path, 'rb') as key_file:
            private_key = RSA.import_key(key_file.read(), passphrase=password)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted_aes_key = cipher_rsa.decrypt(ciphertext)
        return decrypted_aes_key

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES Decryption function, returns decrypted plaintext
        '''
        iv = ciphertext[:AES.block_size]
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        decrypted_plaintext = cipher_aes.decrypt(ciphertext[AES.block_size:])
        padding_length = decrypted_plaintext[-1]
        return decrypted_plaintext[:-padding_length]

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
        # Decode the base64 encoded ciphertext
        decoded_ciphertext = base64.b64decode(encoded_ciphertext)

        # Extract RSA encrypted AES key and AES encrypted data
        # RSA key size is 256 bytes for 2048 bit key
        rsa_encrypted_key = decoded_ciphertext[:256]
        aes_encrypted_data = decoded_ciphertext[256:]

        # Decrypt AES key using RSA
        aes_key = cls._rsa_decrypt(private_key_path, rsa_encrypted_key)

        # Decrypt data using AES
        decrypted_data = cls._aes_decrypt(aes_key, aes_encrypted_data)

        # Convert decrypted data to dictionary
        secrets = json.loads(decrypted_data.decode('utf-8'))
        return secrets
