
import hmac
import hashlib


class Signer:

    def sign(self, msg, key):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf-8')
        if not isinstance(key, bytes):
            key = key.encode('utf-8')
        return hmac.new(key, msg, hashlib.sha256).digest()

    def verify(self, msg, sig, key):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf-8')
        if not isinstance(key, bytes):
            key = key.encode('utf-8')
        expected_sig = hmac.new(key, msg, hashlib.sha256).digest()
        return hmac.compare_digest(expected_sig, sig)
