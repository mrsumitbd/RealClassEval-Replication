
import base64
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
        with open(private_key_path, 'rb') as key_file:
            private_key = RSA.import_key(key_file.read(), passphrase=password)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(base64.b64decode(ciphertext))
        return decrypted

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES Decryption function, returns decrypted plaintext value
        '''
        iv = ciphertext[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
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
        # Step 1: Decode the base64 encoded ciphertext
        decoded_ciphertext = base64.b64decode(encoded_ciphertext)

        # Step 2: Extract the AES key using RSA decryption
        aes_key = cls._rsa_decrypt(private_key_path, decoded_ciphertext[:256])

        # Step 3: Decrypt the remaining data using AES
        decrypted_data = cls._aes_decrypt(aes_key, decoded_ciphertext[256:])

        # Step 4: Split the decrypted data into individual components
        token, token_secret, refresh_token, expires_in = decrypted_data.decode(
            'utf-8').split('\n')

        # Step 5: Return the components in a dictionary
        return {
            "token": token,
            "token_secret": token_secret,
            "refresh_token": refresh_token,
            "expires_in": expires_in
        }
