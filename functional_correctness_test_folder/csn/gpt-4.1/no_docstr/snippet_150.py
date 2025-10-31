
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class MaltegoOauth:

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        if private_key_path is None or ciphertext is None:
            raise ValueError(
                "private_key_path and ciphertext must be provided")
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password.encode() if password else None,
                backend=default_backend()
            )
        decrypted = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        if key is None or ciphertext is None:
            raise ValueError("key and ciphertext must be provided")
        # Assume ciphertext = IV + actual ciphertext
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
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
        if private_key_path is None or encoded_ciphertext is None:
            raise ValueError(
                "private_key_path and encoded_ciphertext must be provided")
        # encoded_ciphertext is base64-encoded: base64(aes_key_encrypted + aes_encrypted_secret)
        decoded = base64.b64decode(encoded_ciphertext)
        # Assume first 256 bytes is RSA-encrypted AES key (for 2048-bit key)
        rsa_encrypted_key = decoded[:256]
        aes_encrypted_secret = decoded[256:]
        aes_key = cls._rsa_decrypt(
            private_key_path=private_key_path, ciphertext=rsa_encrypted_key)
        secret = cls._aes_decrypt(key=aes_key, ciphertext=aes_encrypted_secret)
        return secret
