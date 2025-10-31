import base64
import json
from typing import Optional, Dict, Any

from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asy_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


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
    def _b64decode(data: Optional[str]) -> bytes:
        if data is None:
            raise ValueError("Empty data for base64 decode")
        if isinstance(data, bytes):
            b = data
        else:
            s = data.strip()
            # Try standard b64 with automatic padding
            missing = (-len(s) % 4)
            s_padded = s + ("=" * missing)
            try:
                return base64.b64decode(s_padded, validate=False)
            except Exception:
                # Try urlsafe
                return base64.urlsafe_b64decode(s_padded)
        return b

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        '''
        RSA Decryption function, returns decrypted plaintext in b64 encoding
        '''
        if not private_key_path:
            raise ValueError("private_key_path is required")
        if ciphertext is None:
            raise ValueError("ciphertext is required")

        with open(private_key_path, "rb") as f:
            pem = f.read()

        if isinstance(password, str):
            password_bytes = password.encode("utf-8")
        else:
            password_bytes = password

        private_key = serialization.load_pem_private_key(
            pem, password=password_bytes)

        ct_bytes = MaltegoOauth._b64decode(ciphertext)

        try:
            pt = private_key.decrypt(
                ct_bytes,
                asy_padding.OAEP(
                    mgf=asy_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        except Exception:
            # Fallback to SHA1 OAEP (legacy)
            pt = private_key.decrypt(
                ct_bytes,
                asy_padding.OAEP(
                    mgf=asy_padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None,
                ),
            )
        # Return plaintext in b64 encoding as per docstring
        return base64.b64encode(pt)

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        '''
        AES Decryption function, returns decrypted plaintext value
        '''
        if key is None or ciphertext is None:
            raise ValueError("key and ciphertext are required")

        if isinstance(key, str):
            key_bytes = base64.b64decode(
                key + "===") if all(c.isalnum() or c in "+/=_-" for c in key) else key.encode("utf-8")
            # If it doesn't look like b64, assume utf-8 bytes
            if len(key_bytes) not in (16, 24, 32):
                key_bytes = key.encode("utf-8")
        elif isinstance(key, bytes):
            key_bytes = key
        else:
            raise TypeError("key must be str or bytes")

        ct_bytes = MaltegoOauth._b64decode(ciphertext)

        if len(ct_bytes) < 16:
            raise ValueError("ciphertext is too short, missing IV")
        iv = ct_bytes[:16]
        ct = ct_bytes[16:]

        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ct) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plain = unpadder.update(padded_plain) + unpadder.finalize()
        return plain

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
        if not private_key_path:
            raise ValueError("private_key_path is required")
        if not encoded_ciphertext:
            raise ValueError("encoded_ciphertext is required")

        # Decode outer wrapper (allow raw JSON or b64-encoded JSON)
        raw_bytes: Optional[bytes] = None
        try:
            raw_bytes = cls._b64decode(encoded_ciphertext)
            try:
                payload = json.loads(raw_bytes.decode("utf-8"))
            except Exception:
                # If base64 decode did not yield JSON, try direct JSON
                payload = json.loads(encoded_ciphertext)
        except Exception:
            payload = json.loads(encoded_ciphertext)

        if not isinstance(payload, dict):
            raise ValueError("Invalid ciphertext payload format")

        # Expected payload: {"ek": <b64 RSA-encrypted AES key>, "ct": <b64 AES(iv||ciphertext)>}
        ek = payload.get("ek") or payload.get(
            "encrypted_key") or payload.get("key")
        ct = payload.get("ct") or payload.get(
            "ciphertext") or payload.get("data")

        if not ek or not ct:
            raise ValueError("Payload must contain 'ek' and 'ct'")

        # RSA decrypt to get AES key (function returns b64 plaintext)
        aes_key_b64 = cls._rsa_decrypt(
            private_key_path=private_key_path, ciphertext=ek)
        aes_key = base64.b64decode(aes_key_b64)

        # AES decrypt to get JSON secrets
        secrets_bytes = cls._aes_decrypt(key=aes_key, ciphertext=ct)
        try:
            secrets = json.loads(secrets_bytes.decode("utf-8"))
        except Exception:
            # Fallback: parse pipe-separated string in fixed order
            parts = secrets_bytes.decode("utf-8", errors="ignore").split("|")
            secrets = {}
            if len(parts) >= 1:
                secrets["token"] = parts[0]
            if len(parts) >= 2:
                secrets["token_secret"] = parts[1]
            if len(parts) >= 3:
                secrets["refresh_token"] = parts[2]
            if len(parts) >= 4:
                secrets["expires_in"] = parts[3]

        # Normalize output keys
        result: Dict[str, Any] = {
            "token": secrets.get("token", ""),
            "token_secret": secrets.get("token_secret", secrets.get("tokenSecret", "")),
            "refresh_token": secrets.get("refresh_token", secrets.get("refreshToken", "")),
            "expires_in": str(secrets.get("expires_in", secrets.get("expiresIn", ""))),
        }
        return result
