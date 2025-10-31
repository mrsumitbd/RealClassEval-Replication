
import base64
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


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
                password=password.encode() if password else None,
                backend=default_backend()
            )
        ciphertext_bytes = base64.b64decode(ciphertext)
        plaintext = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES decryption using CBC mode with PKCS7 padding.
        Assumes ciphertext is base64 encoded and IV is prepended (first 16 bytes).
        '''
        ciphertext_bytes = base64.b64decode(ciphertext)
        iv = ciphertext_bytes[:16]
        actual_ciphertext = ciphertext_bytes[16:]
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(
            actual_ciphertext) + decryptor.finalize()
        # Remove PKCS7 padding
        pad_len = padded_plaintext[-1]
        plaintext = padded_plaintext[:-pad_len]
        return plaintext

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
        # The encoded_ciphertext is expected to be a base64-encoded JSON string
        # The JSON contains:
        # {
        #   "key": <base64-encoded RSA-encrypted AES key>,
        #   "data": <base64-encoded AES-encrypted JSON>
        # }
        # The decrypted JSON contains the secrets

        # Step 1: Decode the outer base64 and parse JSON
        decoded = base64.b64decode(encoded_ciphertext)
        payload = json.loads(decoded.decode("utf-8"))

        # Step 2: Decrypt the AES key using RSA
        aes_key = cls._rsa_decrypt(
            private_key_path=private_key_path, ciphertext=payload["key"])

        # Step 3: Decrypt the data using AES
        decrypted_json_bytes = cls._aes_decrypt(
            key=aes_key, ciphertext=payload["data"])
        secrets = json.loads(decrypted_json_bytes.decode("utf-8"))

        # Step 4: Return the secrets in the required format
        return {
            "token": secrets.get("token", ""),
            "token_secret": secrets.get("token_secret", ""),
            "refresh_token": secrets.get("refresh_token", ""),
            "expires_in": secrets.get("expires_in", "")
        }
