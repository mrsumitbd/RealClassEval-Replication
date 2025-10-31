class _RawJWS:

    def sign(self, key, payload):
        raise NotImplementedError

    def verify(self, key, payload, signature):
        raise NotImplementedError