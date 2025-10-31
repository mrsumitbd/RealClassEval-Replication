
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad


class MaltegoOauth:

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        with open(private_key_path, 'rb') as f:
            private_key = RSA.import_key(f.read(), passphrase=password)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher_rsa.decrypt(ciphertext)
        return decrypted_data

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(
            actual_ciphertext), AES.block_size)
        return decrypted_data

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        decoded_ciphertext = base64.b64decode(encoded_ciphertext)
        rsa_ciphertext = decoded_ciphertext[:256]
        aes_ciphertext = decoded_ciphertext[256:]
        aes_key = cls._rsa_decrypt(private_key_path, rsa_ciphertext)
        decrypted_secret = cls._aes_decrypt(aes_key, aes_ciphertext)
        return decrypted_secret.decode('utf-8')
