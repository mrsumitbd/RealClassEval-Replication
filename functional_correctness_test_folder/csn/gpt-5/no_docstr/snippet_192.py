class CONCATENATE_BASE_AND_KEY_Mechanism:

    def __init__(self, encKey):
        if isinstance(encKey, bytearray):
            encKey = bytes(encKey)
        if not isinstance(encKey, (str, bytes)):
            raise TypeError("encKey must be str or bytes")
        self.encKey = encKey

    def to_native(self):
        encKey = self.encKey

        def concatenate(base):
            if isinstance(base, bytearray):
                base = bytes(base)
            if not isinstance(base, (str, bytes)):
                raise TypeError("base must be str or bytes")
            if isinstance(base, str) and isinstance(encKey, str):
                return base + encKey
            if isinstance(base, bytes) and isinstance(encKey, bytes):
                return base + encKey
            raise TypeError(
                "Type mismatch: base and encKey must both be str or both be bytes")

        return concatenate
