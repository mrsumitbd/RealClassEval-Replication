
import hmac
import hashlib


class Signer:

    def sign(self, msg, key):
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        signature = hmac.new(key, msg, hashlib.sha256).hexdigest()
        return signature

    def verify(self, msg, sig, key):
        expected_sig = self.sign(msg, key)
        return hmac.compare_digest(expected_sig, sig)
