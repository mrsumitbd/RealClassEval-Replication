
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
        decrypted = cipher.decrypt(base64.b64decode(ciphertext))
        return base64.b64encode(decrypted).decode('utf-8')

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        cipher = AES.new(base64.b64decode(key), AES.MODE_ECB)
        decrypted = cipher.decrypt(base64.b64decode(ciphertext))
        return decrypted.decode('utf-8').rstrip('\0')

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
        decrypted = cls._rsa_decrypt(private_key_path, encoded_ciphertext)
        decrypted_dict = json.loads(
            cls._aes_decrypt(decrypted, encoded_ciphertext))
        return decrypted_dict
