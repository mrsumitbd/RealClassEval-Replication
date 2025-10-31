class Signer:
    def _to_bytes(self, x):
        if isinstance(x, bytes):
            return x
        if isinstance(x, bytearray):
            return bytes(x)
        return str(x).encode("utf-8")

    def sign(self, msg, key):
        import hmac
        import hashlib
        k = self._to_bytes(key)
        m = self._to_bytes(msg)
        return hmac.new(k, m, hashlib.sha256).hexdigest()

    def verify(self, msg, sig, key):
        import hmac
        import hashlib
        k = self._to_bytes(key)
        m = self._to_bytes(msg)
        mac = hmac.new(k, m, hashlib.sha256)
        expected_hex = mac.hexdigest()
        expected_raw = mac.digest()

        # Accept raw bytes or hex string
        if isinstance(sig, (bytes, bytearray)):
            s = bytes(sig)
            if len(s) == len(expected_raw):
                return hmac.compare_digest(s, expected_raw)
            try:
                s_str = s.decode("ascii")
            except Exception:
                return False
            return hmac.compare_digest(s_str.lower(), expected_hex)
        else:
            s_str = str(sig)
            return hmac.compare_digest(s_str.lower(), expected_hex)
