
import hashlib
import hmac


class Signer:

    def sign(self, msg, key):
        """Generate a digital signature for a given message using a secret key."""
        return hmac.new(key, msg.encode(), hashlib.sha256).digest()

    def verify(self, msg, sig, key):
        """Verify a digital signature for a given message using a secret key."""
        expected_sig = self.sign(msg, key)
        return hmac.compare_digest(sig, expected_sig)
