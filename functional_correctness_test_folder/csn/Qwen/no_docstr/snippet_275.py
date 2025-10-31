
import hmac
import hashlib


class Signer:

    def sign(self, msg, key):
        return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

    def verify(self, msg, sig, key):
        return hmac.compare_digest(self.sign(msg, key), sig)
