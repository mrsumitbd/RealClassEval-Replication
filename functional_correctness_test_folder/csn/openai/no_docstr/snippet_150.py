
import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class MaltegoOauth:
    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        """
        Decrypts a ciphertext using an RSA private key.

        :param private_key_path: Path to the PEM-encoded private key file.
        :param ciphertext: Bytes to decrypt.
        :param password: Optional password for encrypted private key.
        :return: Decrypted bytes.
        """
        if not private_key_path or not ciphertext:
            return None

        key_data = Path(private_key_path).read_bytes()
        private_key = serialization.load_pem_private_key(
            key_data, password=password, backend=default_backend()
        )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise TypeError("Provided key is not an RSA private key")

        decrypted = private_key.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=serialization.hashes.SHA256()),
                algorithm=serialization.hashes.SHA256(),
                label=None,
            ),
        )
        return decrypted

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        """
        Decrypts a ciphertext using AES-CBC with PKCS7 padding.

        The ciphertext is expected to be IV (16 bytes) + encrypted data.

        :param key: AES key bytes.
        :param ciphertext: Bytes to decrypt.
        :return: Decrypted bytes.
        """
        if not key or not ciphertext or len(ciphertext) <= 16:
            return None

        iv = ciphertext[:16]
        enc_data = ciphertext[16:]

        cipher = Cipher(
            algorithms.AES(key), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(enc_data) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plain = unpadder.update(padded_plain) + unpadder.finalize()
        return plain

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        """
        Decrypts secrets that were encrypted with a hybrid RSA/AES scheme.

        The encoded_ciphertext is a base64 string containing:
          - RSA-encrypted AES key (size depends on key length, e.g., 256 bytes for 2048-bit key)
          - AES-encrypted payload (IV + ciphertext)

        :param private_key_path: Path to the PEM-encoded RSA private key.
        :param encoded_ciphertext: Base64-encoded string of the hybrid ciphertext.
        :return: Decrypted plaintext as a string (UTF-8 decoded).
        """
        if not private_key_path or not encoded_ciphertext:
            return None

        raw = base64.b64decode(encoded_ciphertext)

        # Determine RSA key size from the private key
        key_data = Path(private_key_path).read_bytes()
        private_key = serialization.load_pem_private_key(
            key_data, password=None, backend=default_backend()
        )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise TypeError("Provided key is not an RSA private key")

        key_size_bytes = private_key.key_size // 8
        if len(raw) < key_size_bytes:
            raise ValueError("Ciphertext too short for RSA key size")

        rsa_encrypted_key = raw[:key_size_bytes]
        aes_ciphertext = raw[key_size_bytes:]

        aes_key = cls._rsa_decrypt(private_key_path, rsa_encrypted_key)
        if aes_key is None:
            raise ValueError("Failed to decrypt AES key with RSA")

        plaintext_bytes = cls._aes_decrypt(aes_key, aes_ciphertext)
        if plaintext_bytes is None:
            raise ValueError("Failed to decrypt AES payload")

        return plaintext_bytes.decode("utf-8")
