class EventWebhook:

    def __init__(self, public_key=None):
        self._public_key_raw = public_key
        self._verifying_key = None
        if public_key is not None:
            self._verifying_key = self.convert_public_key_to_ecdsa(public_key)

    def convert_public_key_to_ecdsa(self, public_key):
        import base64
        import textwrap
        try:
            import ecdsa
        except Exception as e:
            raise RuntimeError(
                "ecdsa package is required to use EventWebhook") from e

        if isinstance(public_key, ecdsa.VerifyingKey):
            return public_key

        if isinstance(public_key, bytes):
            public_key = public_key.decode("utf-8")

        public_key = public_key.strip()

        if "BEGIN PUBLIC KEY" in public_key:
            pem = public_key
        else:
            # Assume base64-encoded DER SubjectPublicKeyInfo
            b64_clean = "".join(public_key.split())
            pem = "-----BEGIN PUBLIC KEY-----\n"
            pem += "\n".join(textwrap.wrap(b64_clean, 64))
            pem += "\n-----END PUBLIC KEY-----\n"

        try:
            vk = ecdsa.VerifyingKey.from_pem(pem)
        except Exception as e:
            raise ValueError("Invalid public key") from e
        return vk

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        import base64
        import hashlib
        try:
            import ecdsa
        except Exception:
            return False

        vk = None
        if public_key is not None:
            try:
                vk = self.convert_public_key_to_ecdsa(public_key)
            except Exception:
                return False
        elif self._verifying_key is not None:
            vk = self._verifying_key
        else:
            return False

        if isinstance(payload, bytes):
            payload_bytes = payload
        else:
            payload_bytes = str(payload).encode("utf-8")

        ts_str = str(timestamp)
        sig_b: bytes
        try:
            sig_b = base64.b64decode(signature, validate=True)
        except Exception:
            return False

        # Build candidate messages (compatibility with known variants)
        candidates = [
            # timestamp + payload
            ts_str.encode("utf-8") + payload_bytes,
            # timestamp.payload
            f"{ts_str}.{payload_bytes.decode('utf-8', errors='ignore')}".encode(
                "utf-8"),
        ]

        # Try DER-encoded signature first (expected)
        for msg in candidates:
            try:
                if vk.verify(sig_b, msg, hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der):
                    return True
            except Exception:
                pass

        # Fallback: try raw (r||s) signature format if ever encountered
        for msg in candidates:
            try:
                if vk.verify(sig_b, msg, hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_string):
                    return True
            except Exception:
                pass

        return False
