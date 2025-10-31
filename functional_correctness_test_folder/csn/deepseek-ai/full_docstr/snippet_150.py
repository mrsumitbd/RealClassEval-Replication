
import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad


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
        with open(private_key_path, 'rb') as f:
            private_key = RSA.import_key(f.read(), passphrase=password)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(base64.b64decode(ciphertext))
        return decrypted

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES Decryption function, returns decrypted plaintext value
        '''
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted

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
        decoded = base64.b64decode(encoded_ciphertext)
        parts = decoded.split(b':', 1)
        if len(parts) != 2:
            raise ValueError("Invalid ciphertext format")

        rsa_encrypted_aes_key = parts[0]
        aes_encrypted_data = parts[1]

        aes_key = cls._rsa_decrypt(private_key_path, rsa_encrypted_aes_key)
        decrypted_data = cls._aes_decrypt(aes_key, aes_encrypted_data)

        secrets = json.loads(decrypted_data.decode('utf-8'))
        return {
            "token": secrets.get("token", ""),
            "token_secret": secrets.get("token_secret", ""),
            "refresh_token": secrets.get("refresh_token", ""),
            "expires_in": secrets.get("expires_in", "")
        }
