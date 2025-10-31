
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
        rsa_encrypted_aes_key = decoded[:256]
        aes_encrypted_data = decoded[256:]

        aes_key = cls._rsa_decrypt(
            private_key_path, base64.b64encode(rsa_encrypted_aes_key))
        decrypted_data = cls._aes_decrypt(aes_key, aes_encrypted_data)

        data = json.loads(decrypted_data.decode('utf-8'))
        return {
            "token": data.get("token", ""),
            "token_secret": data.get("token_secret", ""),
            "refresh_token": data.get("refresh_token", ""),
            "expires_in": data.get("expires_in", "")
        }
