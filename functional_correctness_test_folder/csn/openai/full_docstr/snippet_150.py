
import base64
import json
from pathlib import Path
from typing import Dict, Optional

from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend


class MaltegoOauth:
    """
    A Crypto Helper for Maltego OAuth Secrets received from the Transform Distribution Server
    The TDS will send back an encrypted combination of the following :
    1. Token
    2. Token Secret
    3. Refresh Token
    4. Expires In
    Contains Methods:
        1. decrypt_secrets(private_key_path="pem file", ciphertext="request.getTransformSetting('name from TDS')")
    """

    @staticmethod
    def _rsa_decrypt(
        private_key_path: Optional[str] = None,
        ciphertext: Optional[str] = None,
        password: Optional[bytes] = None,
    ) -> bytes:
        """
        RSA Decryption function, returns decrypted plaintext in bytes
        """
        if not private_key_path or not ciphertext:
            raise ValueError(
                "private_key_path and ciphertext must be provided")

        key_data = Path(private_key_path).read_bytes()
        private_key = load_pem_private_key(
            key_data, password=password, backend=default_backend())

        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise TypeError("Provided key is not an RSA private key")

        encrypted_bytes = base64.b64decode(ciphertext)
        plaintext = private_key.decrypt(
            encrypted_bytes,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext

    @staticmethod
    def _aes_decrypt(key: bytes, ciphertext: bytes) -> bytes:
        """
        AES Decryption function, returns decrypted plaintext value
        """
        if not key or not ciphertext:
            raise ValueError("key and ciphertext must be provided")

        # Assume AES-256-CBC with IV prepended to ciphertext
        iv = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ct) + decryptor.finalize()

        # PKCS7 unpadding
        unpadder = sym_padding.PKCS7(128).unpadder()
        plain = unpadder.update(padded_plain) + unpadder.finalize()
        return plain

    @classmethod
    def decrypt_secrets(
        cls,
        private_key_path: Optional[str] = None,
        encoded_ciphertext: Optional[str] = None,
    ) -> Dict[str, str]:
        """
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
        """
        if not private_key_path or not encoded_ciphertext:
            raise ValueError(
                "private_key_path and encoded_ciphertext must be provided")

        # Step 1: RSA decrypt to get the AES key and the encrypted payload
        # We expect the RSA decrypted payload to be a JSON string with two fields:
        #   "aes_key": base64-encoded AES key
        #   "payload": base64-encoded AES-encrypted JSON of secrets
        rsa_plain = cls._rsa_decrypt(private_key_path, encoded_ciphertext)

        try:
            rsa_json = json.loads(rsa_plain.decode("utf-8"))
            aes_key_b64 = rsa_json.get("aes_key")
            payload_b64 = rsa_json.get("payload")
            if not aes_key_b64 or not payload_b64:
                raise ValueError(
                    "Missing aes_key or payload in RSA decrypted data")
        except Exception as exc:
            raise ValueError(
                f"Failed to parse RSA decrypted data: {exc}") from exc

        aes_key = base64.b64decode(aes_key_b64)
        payload_bytes = base64.b64decode(payload_b64)

        # Step 2: AES decrypt the payload
        try:
            secrets_plain = cls._aes_decrypt(aes_key, payload_bytes)
            secrets_dict = json.loads(secrets_plain.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"Failed to decrypt AES payload: {exc}") from exc

        # Ensure all required keys are present
        required_keys = {"token", "token_secret",
                         "refresh_token", "expires_in"}
        if not required_keys.issubset(secrets_dict.keys()):
            missing = required_keys - secrets_dict.keys()
            raise ValueError(f"Missing keys in secrets payload: {missing}")

        return {
            "token": str(secrets_dict["token"]),
            "token_secret": str(secrets_dict["token_secret"]),
            "refresh_token": str(secrets_dict["refresh_token"]),
            "expires_in": str(secrets_dict["expires_in"]),
        }
