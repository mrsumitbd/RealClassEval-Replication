class _RawKeyMgmt:

    def wrap(self, key, bitsize, cek, headers):
        raise NotImplementedError

    def unwrap(self, key, bitsize, ek, headers):
        raise NotImplementedError