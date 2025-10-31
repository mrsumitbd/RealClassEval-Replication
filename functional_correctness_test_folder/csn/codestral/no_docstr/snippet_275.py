
class Signer:

    def sign(self, msg, key):
        import hashlib
        import hmac
        signature = hmac.new(key.encode(), msg.encode(),
                             hashlib.sha256).hexdigest()
        return signature

    def verify(self, msg, sig, key):
        import hashlib
        import hmac
        new_sig = hmac.new(key.encode(), msg.encode(),
                           hashlib.sha256).hexdigest()
        return hmac.compare_digest(new_sig, sig)
