import base64
import json
from typing import Optional, Union

from cryptography.hazmat.primitives import hashes, serialization, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class MaltegoOauth:
    @staticmethod
    def _to_bytes(data: Union[str, bytes, bytearray, None]) -> Optional[bytes]:
        if data is None:
            return None
        if isinstance(data, bytes):
            return data
        if isinstance(data, bytearray):
            return bytes(data)
        if isinstance(data, str):
            return data.encode("utf-8")
        raise TypeError("Unsupported data type; expected str/bytes/bytearray")

    @staticmethod
    def _b64_to_bytes(maybe_b64: Union[str, bytes]) -> bytes:
        if isinstance(maybe_b64, bytes):
            s = maybe_b64
        else:
            s = maybe_b64.encode("utf-8")
        try:
            return base64.b64decode(s, validate=True)
        except Exception:
            # Not valid base64, return as-is assuming it is raw bytes
            return s

    @staticmethod
    def _rsa_decrypt(private_key_path=None, ciphertext=None, password=None):
        if not private_key_path:
            raise ValueError("private_key_path is required")
        if ciphertext is None:
            raise ValueError("ciphertext is required")

        with open(private_key_path, "rb") as f:
            pem = f.read()

        pwd_bytes = None
        if password is not None:
            pwd_bytes = MaltegoOauth._to_bytes(password)

        private_key = serialization.load_pem_private_key(
            pem, password=pwd_bytes)

        ct_bytes = MaltegoOauth._b64_to_bytes(ciphertext)

        try:
            return private_key.decrypt(
                ct_bytes,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        except Exception:
            # Fallback to PKCS1v15 if OAEP fails
            return private_key.decrypt(ct_bytes, asym_padding.PKCS1v15())

    @staticmethod
    def _aes_decrypt(key=None, ciphertext=None):
        if key is None:
            raise ValueError("key is required")
        key_bytes = MaltegoOauth._to_bytes(key)

        # Accept ciphertext as:
        # - dict with keys: iv, ct/ciphertext, tag (GCM)
        # - dict with iv, ct (CBC-PKCS7) if no tag provided
        # - bytes with layout [iv|ct|tag] where iv=12, tag=16 for GCM
        # - base64 string of the above bytes
        if isinstance(ciphertext, (str, bytes, bytearray)):
            # iv|ct|tag (GCM) or iv|ct (CBC cannot be inferred)
            blob = MaltegoOauth._b64_to_bytes(ciphertext)
            if len(blob) >= 12 + 16 + 1:  # assume GCM with 12-byte IV, 16-byte tag
                iv = blob[:12]
                tag = blob[-16:]
                ct = blob[12:-16]
                decryptor = Cipher(algorithms.AES(key_bytes),
                                   modes.GCM(iv, tag)).decryptor()
                return decryptor.update(ct) + decryptor.finalize()
            else:
                raise ValueError(
                    "Ciphertext bytes format unsupported or too short")
        elif isinstance(ciphertext, dict):
            # Normalize keys
            iv_b64 = ciphertext.get("iv") or ciphertext.get("nonce")
            ct_b64 = ciphertext.get("ct") or ciphertext.get(
                "ciphertext") or ciphertext.get("data")
            tag_b64 = ciphertext.get("tag") or ciphertext.get(
                "auth_tag") or ciphertext.get("mac")

            if iv_b64 is None or ct_b64 is None:
                raise ValueError(
                    "ciphertext dict must contain at least iv and ct/ciphertext/data")

            iv = MaltegoOauth._b64_to_bytes(iv_b64)
            ct = MaltegoOauth._b64_to_bytes(ct_b64)

            if tag_b64 is not None:
                tag = MaltegoOauth._b64_to_bytes(tag_b64)
                decryptor = Cipher(algorithms.AES(key_bytes),
                                   modes.GCM(iv, tag)).decryptor()
                return decryptor.update(ct) + decryptor.finalize()
            else:
                # CBC with PKCS7 padding if no tag provided
                if len(iv) not in (16,):
                    raise ValueError("CBC mode requires a 16-byte IV")
                decryptor = Cipher(algorithms.AES(key_bytes),
                                   modes.CBC(iv)).decryptor()
                padded = decryptor.update(ct) + decryptor.finalize()
                unpadder = sym_padding.PKCS7(128).unpadder()
                return unpadder.update(padded) + unpadder.finalize()
        else:
            raise TypeError("Unsupported ciphertext type")

    @classmethod
    def decrypt_secrets(cls, private_key_path=None, encoded_ciphertext=None):
        if encoded_ciphertext is None:
            raise ValueError("encoded_ciphertext is required")

        # encoded_ciphertext is expected to be base64 of a JSON payload or a dict already
        payload = None
        if isinstance(encoded_ciphertext, dict):
            payload = encoded_ciphertext
        else:
            raw = cls._b64_to_bytes(encoded_ciphertext)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except Exception:
                # If not JSON after b64-decode, try direct JSON parse
                if isinstance(encoded_ciphertext, (bytes, bytearray)):
                    text = bytes(encoded_ciphertext).decode("utf-8")
                else:
                    text = str(encoded_ciphertext)
                payload = json.loads(text)

        # Expected fields:
        # - RSA-encrypted AES key: one of ["encrypted_key", "ek", "key"]
        # - AES payload: iv/nonce, ct/ciphertext/data, tag (optional for CBC)
        enc_key_b64 = payload.get("encrypted_key") or payload.get(
            "ek") or payload.get("key")
        if enc_key_b64 is None:
            raise ValueError("No encrypted symmetric key found in payload")

        aes_key = cls._rsa_decrypt(
            private_key_path=private_key_path, ciphertext=enc_key_b64)

        # Decrypt AES payload
        # Accept both nested structure under "payload" or top-level fields
        aes_payload = payload.get("payload") or payload

        plaintext = cls._aes_decrypt(key=aes_key, ciphertext=aes_payload)

        # Try decode to text; if fails, return raw bytes
        try:
            return plaintext.decode("utf-8")
        except Exception:
            return plaintext
