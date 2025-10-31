
import hmac
import hashlib
import base64


class Signer:
    def sign(self, msg, key):
        if isinstance(msg, str):
            msg = msg.encode()
        if isinstance(key, str):
            key = key.encode()
        digest = hmac.new(key, msg, hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def verify(self, msg, sig, key):
        if isinstance(msg, str):
            msg = msg.encode()
        if isinstance(key, str):
            key = key.encode()
        expected = hmac.new(key, msg, hashlib.sha256).digest()
        try:
            sig_bytes = base64.b64decode(sig)
        except Exception:
            return False
        return hmac.compare_digest(expected, sig_bytes)
