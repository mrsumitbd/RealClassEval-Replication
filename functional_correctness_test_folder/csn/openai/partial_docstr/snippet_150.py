
import base64
import json
from pathlib import Path
from typing import Dict, Optional

from cryptography.hazmat.primitives import hashes, padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class MaltegoOauth:
    """
    A Crypto Helper for Maltego OAuth Secrets received from the Transform Distribution Server.
    The TDS will send back an encrypted combination of the following:
    1. Token
    2. Token Secret
    3. Refresh Token
    4. Expires In
    Contains Methods:
        1. decrypt_secrets(private_key_path="pem file",
                            encoded_ciphertext="request.getTransformSetting('name from TDS')")
    """

    @staticmethod
    def _rsa_decrypt(
        private_key_path: Optional[str] = None,
        ciphertext: Optional[str] = None,
        password: Optional[bytes] = None,
    ) -> bytes:
        """
        RSA Decryption function, returns decrypted plaintext bytes.
        The ciphertext is expected to be base64 encoded.
        """
        if not private_key_path or not ciphertext:
            raise ValueError(
                "private_key_path and ciphertext must be provided")

        # Load private key
        key_data = Path(private_key_path).read_bytes()
        private_key = serialization.load_pem_private_key(
            key_data, password=password, backend=default_backend()
        )

        # Decode ciphertext
        ct_bytes = base64.b64decode(ciphertext)

        # Decrypt
        plaintext = private_key.decrypt(
            ct_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
            ),
        )
        return plaintext

    @staticmethod
    def _aes_decrypt(key: bytes, ciphertext: bytes) -> bytes:
        """
        AES decryption function.
        The ciphertext is expected to be base64 encoded and to contain the IV as the first 16 bytes.
        """
        if not key or not ciphertext:
            raise ValueError("key and ciphertext must be provided")

        # Decode ciphertext
        ct_bytes = base64.b64decode(ciphertext)

        # Extract IV and actual ciphertext
        iv = ct_bytes[:16]
        ct = ct_bytes[16:]

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ct) + decryptor.finalize()

        # Unpad
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext

    @classmethod
    def decrypt_secrets(
        cls,
        private_key_path: Optional[str] = None,
        encoded_ciphertext: Optional[str] = None,
        password: Optional[bytes] = None,
    ) -> Dict[str, str]:
        """
        The TDS will send back an encrypted combination of the following:
        1. Token
        2. Token Secret
        3. Refresh Token
        4. Expires In
        This function decodes the combinations and decrypts as required and returns a dictionary with the following keys
            {"token":"", "token_secret":"", "refresh_token":"", "expires_in":""}
        """
        if not private_key_path or not encoded_ciphertext:
            raise ValueError(
                "private_key_path and encoded_ciphertext must be provided")

        # First, RSA decrypt to get the AES key and the AES encrypted payload
        # We assume the RSA encrypted payload is a JSON string containing:
        #   {"aes_key":"<base64>", "payload":"<base64>"}
        try:
            rsa_plaintext = cls._rsa_decrypt(
                private_key_path=private_key_path,
                ciphertext=encoded_ciphertext,
                password=password,
            )
            rsa_json = json.loads(rsa_plaintext.decode("utf-8"))
            aes_key_b64 = rsa_json.get("aes_key")
            payload_b64 = rsa_json.get("payload")
            if not aes_key_b64 or not payload_b64:
                raise ValueError("Invalid RSA payload structure")
            aes_key = base64.b64decode(aes_key_b64)
        except Exception as e:
            raise ValueError(f"RSA decryption failed: {e}")

        # Now AES decrypt the payload
        try:
            aes_plaintext = cls._aes_decrypt(
                key=aes_key, ciphertext=payload_b64)
            payload_json = json.loads(aes_plaintext.decode("utf-8"))
        except Exception as e:
            raise ValueError(f"AES decryption failed: {e}")

        # Extract required fields
        result = {
            "token": payload_json.get("token", ""),
            "token_secret": payload_json.get("token_secret", ""),
            "refresh_token": payload_json.get("refresh_token", ""),
            "expires_in": payload_json.get("expires_in", ""),
        }
        return result
