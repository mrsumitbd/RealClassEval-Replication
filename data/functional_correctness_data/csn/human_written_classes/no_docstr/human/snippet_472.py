class _RawJWE:

    def encrypt(self, k, aad, m):
        raise NotImplementedError

    def decrypt(self, k, aad, iv, e, t):
        raise NotImplementedError