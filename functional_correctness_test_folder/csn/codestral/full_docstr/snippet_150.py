
import base64
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


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
        with open(private_key_path, 'r') as f:
            private_key = RSA.import_key(f.read(), passphrase=password)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        return base64.b64encode(decrypted_data).decode('utf-8')

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES Decryption function, returns decrypted plaintext value
        '''
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        return decrypted_data.decode('utf-8').strip()

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
        decrypted_data = cls._rsa_decrypt(private_key_path, encoded_ciphertext)
        decrypted_data = json.loads(decrypted_data)
        decrypted_secrets = {
            "token": cls._aes_decrypt(base64.b64decode(decrypted_data["key"]), decrypted_data["token"]),
            "token_secret": cls._aes_decrypt(base64.b64decode(decrypted_data["key"]), decrypted_data["token_secret"]),
            "refresh_token": cls._aes_decrypt(base64.b64decode(decrypted_data["key"]), decrypted_data["refresh_token"]),
            "expires_in": cls._aes_decrypt(base64.b64decode(decrypted_data["key"]), decrypted_data["expires_in"])
        }
        return decrypted_secrets
