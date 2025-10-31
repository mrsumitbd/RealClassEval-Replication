import base64
import json
from typing import Any, Dict, Optional

try:
    from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
    from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception as e:  # pragma: no cover
    serialization = None  # type: ignore


def _b64_decode(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        s = data
    else:
        s = str(data).encode("utf-8")
    s = s.strip().replace(b" ", b"")
    # add padding if missing
    rem = len(s) % 4
    if rem:
        s += b"=" * (4 - rem)
    try:
        return base64.b64decode(s, validate=False)
    except Exception:
        # try urlsafe
        return base64.urlsafe_b64decode(s)


def _b64_encode(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")


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
        if serialization is None:
            raise RuntimeError(
                "cryptography package is required for RSA decryption")
        if not private_key_path:
            raise ValueError("private_key_path is required")
        if ciphertext is None:
            raise ValueError("ciphertext is required")

        with open(private_key_path, "rb") as f:
            pem_data = f.read()

        if isinstance(password, str):
            pw_bytes = password.encode("utf-8")
        else:
            pw_bytes = password

        private_key = serialization.load_pem_private_key(
            pem_data, password=pw_bytes, backend=default_backend())

        ct_bytes = _b64_decode(ciphertext)

        # Try OAEP(SHA256) then fall back to PKCS1v15 for compatibility
        plaintext: Optional[bytes] = None
        try:
            plaintext = private_key.decrypt(
                ct_bytes,
                asym_padding.OAEP(mgf=asym_padding.MGF1(
                    algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
            )
        except Exception:
            try:
                plaintext = private_key.decrypt(
                    ct_bytes, asym_padding.PKCS1v15())
            except Exception as e:
                raise ValueError("RSA decryption failed") from e

        return _b64_encode(plaintext)

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        if key is None:
            raise ValueError("key is required")
        if ciphertext is None:
            raise ValueError("ciphertext is required")

        # key may already be bytes or an encoded base64 string
        if isinstance(key, (bytes, bytearray)):
            key_bytes = bytes(key)
        else:
            # if given as base64-encoded string, decode
            try:
                key_bytes = _b64_decode(key)
            except Exception:
                key_bytes = str(key).encode("utf-8")

        # normalize length to 16/24/32
        if len(key_bytes) not in (16, 24, 32):
            # attempt to hash-down to 32 bytes for robustness
            try:
                from cryptography.hazmat.primitives import hashes as _hashes

                digest = _hashes.Hash(
                    _hashes.SHA256(), backend=default_backend())
                digest.update(key_bytes)
                key_bytes = digest.finalize()
            except Exception:
                pass

        ct_text = ciphertext if isinstance(
            ciphertext, str) else ciphertext.decode("utf-8", errors="ignore")
        ct_text = ct_text.strip()

        # Possible formats:
        # 1) "iv_b64:ciphertext_b64"  (AES-CBC)
        # 2) "iv_b64:ciphertext_b64:tag_b64" (AES-GCM)
        # 3) "ciphertext_b64" where first 16 raw bytes after b64-decoding are IV (CBC)
        parts = ct_text.split(":")
        plaintext: Optional[bytes] = None

        try:
            if len(parts) == 3:
                iv = _b64_decode(parts[0])
                ct = _b64_decode(parts[1])
                tag = _b64_decode(parts[2])
                aesgcm = AESGCM(key_bytes)
                plaintext = aesgcm.decrypt(iv, ct + tag, None)
                return plaintext
            elif len(parts) == 2:
                iv = _b64_decode(parts[0])
                ct = _b64_decode(parts[1])
                cipher = Cipher(algorithms.AES(key_bytes),
                                modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                padded = decryptor.update(ct) + decryptor.finalize()
                unpadder = sym_padding.PKCS7(128).unpadder()
                plaintext = unpadder.update(padded) + unpadder.finalize()
                return plaintext
        except Exception:
            plaintext = None

        # Fallback: assume b64, IV prefixed to ciphertext (first 16 bytes)
        raw = _b64_decode(ct_text)
        if len(raw) < 17:
            raise ValueError("Invalid AES ciphertext")

        iv = raw[:16]
        ct = raw[16:]
        cipher = Cipher(algorithms.AES(key_bytes),
                        modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ct) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
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
        if not private_key_path:
            raise ValueError("private_key_path is required")
        if not encoded_ciphertext:
            raise ValueError("encoded_ciphertext is required")

        # Attempt to decode the envelope
        payload_obj: Dict[str, Any] = {}
        raw_bytes: Optional[bytes] = None

        # Try base64 -> json
        try:
            raw_bytes = _b64_decode(encoded_ciphertext)
            payload_obj = json.loads(raw_bytes.decode("utf-8"))
        except Exception:
            # Maybe it's already JSON
            try:
                payload_obj = json.loads(encoded_ciphertext if isinstance(
                    encoded_ciphertext, str) else encoded_ciphertext.decode("utf-8"))
            except Exception:
                payload_obj = {}

        rsa_ct_b64: Optional[str] = None
        aes_ct_repr: Optional[str] = None

        # Common key names
        for k in ("key", "aes_key", "encrypted_key", "rsa", "rsa_key"):
            if k in payload_obj:
                rsa_ct_b64 = payload_obj[k]
                break
        for k in ("ciphertext", "secrets", "payload", "data", "ct"):
            if k in payload_obj:
                aes_ct_repr = payload_obj[k]
                break

        # If not JSON, attempt delimited format: "<rsa_b64>|<aes_ct_repr>"
        if rsa_ct_b64 is None or aes_ct_repr is None:
            s = encoded_ciphertext if isinstance(
                encoded_ciphertext, str) else encoded_ciphertext.decode("utf-8", errors="ignore")
            # Try to decode base64 first to see if it's "rsa:...:aes:..."
            if "|" in s:
                parts = s.split("|", 1)
                if len(parts) == 2:
                    rsa_ct_b64 = parts[0].strip()
                    aes_ct_repr = parts[1].strip()
            elif ":" in s and len(s.split(":")) >= 4:
                # Heuristic: rsa_b64 : aes_iv_b64 : aes_ct_b64 [ : gcm_tag_b64 ]
                # So first token is rsa, remainder join as aes repr
                parts = s.split(":")
                rsa_ct_b64 = parts[0].strip()
                aes_ct_repr = ":".join(parts[1:]).strip()

        if rsa_ct_b64 is None or aes_ct_repr is None:
            raise ValueError("Unable to parse encoded_ciphertext payload")

        # 1) Decrypt RSA to get AES key (returned in b64 per _rsa_decrypt)
        aes_key_b64 = cls._rsa_decrypt(
            private_key_path=private_key_path, ciphertext=rsa_ct_b64)
        aes_key = _b64_decode(aes_key_b64)

        # 2) AES decrypt secrets payload
        secrets_bytes = cls._aes_decrypt(key=aes_key, ciphertext=aes_ct_repr)
        secrets_text = secrets_bytes.decode("utf-8", errors="ignore").strip()

        # 3) Parse secrets as JSON or delimited string
        result = {
            "token": "",
            "token_secret": "",
            "refresh_token": "",
            "expires_in": "",
        }

        parsed = None
        try:
            parsed = json.loads(secrets_text)
        except Exception:
            parsed = None

        if isinstance(parsed, dict):
            result["token"] = str(parsed.get("token", "")) if parsed.get(
                "token") is not None else ""
            result["token_secret"] = str(parsed.get("token_secret", "")) if parsed.get(
                "token_secret") is not None else ""
            result["refresh_token"] = str(parsed.get("refresh_token", "")) if parsed.get(
                "refresh_token") is not None else ""
            result["expires_in"] = str(parsed.get("expires_in", "")) if parsed.get(
                "expires_in") is not None else ""
            # Accept alternative keys
            if not result["token"] and "access_token" in parsed:
                result["token"] = str(parsed.get("access_token", ""))
            if not result["token_secret"] and "secret" in parsed:
                result["token_secret"] = str(parsed.get("secret", ""))
            if not result["expires_in"] and "expiry" in parsed:
                result["expires_in"] = str(parsed.get("expiry", ""))
            return result

        # Fallback: pipe/comma separated order: token|token_secret|refresh_token|expires_in
        delim = "|"
        if delim not in secrets_text:
            delim = "," if "," in secrets_text else None
        if delim:
            parts = [p.strip() for p in secrets_text.split(delim)]
            if len(parts) >= 1:
                result["token"] = parts[0]
            if len(parts) >= 2:
                result["token_secret"] = parts[1]
            if len(parts) >= 3:
                result["refresh_token"] = parts[2]
            if len(parts) >= 4:
                result["expires_in"] = parts[3]
        else:
            # If we cannot parse, return plaintext as token
            result["token"] = secrets_text

        return result
