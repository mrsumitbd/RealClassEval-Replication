
import base64
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


class MaltegoOauth:

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        with open(private_key_path, 'r') as f:
            private_key = RSA.import_key(f.read(), passphrase=password)
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(ciphertext)

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        cipher = AES.new(key, AES.MODE_GCM, nonce=ciphertext[:16])
        plaintext, _ = cipher.decrypt_and_verify(
            ciphertext[16:-16], ciphertext[-16:])
        return plaintext

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        ciphertext = base64.b64decode(encoded_ciphertext)
        secrets = json.loads(cls._aes_decrypt(cls._rsa_decrypt(
            private_key_path, ciphertext[:256]), ciphertext[256:]))
        return secrets
