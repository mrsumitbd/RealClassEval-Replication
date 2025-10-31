class AESModeCTR:

    def __init__(self, key, iv):
        try:
            from Crypto.Cipher import AES  # noqa: F401
            from Crypto.Util import Counter  # noqa: F401
        except ImportError:
            raise ImportError(
                "PyCryptodome is required. Install with: pip install pycryptodome")
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes")
        if len(key) not in (16, 24, 32):
            raise ValueError("key must be 16, 24, or 32 bytes")
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes")
        if len(iv) != 16:
            raise ValueError(
                "iv must be 16 bytes for AES-CTR initial counter value")
        self._key = bytes(key)
        self._iv = bytes(iv)

    def _new_cipher(self):
        from Crypto.Cipher import AES
        from Crypto.Util import Counter
        initial_value = int.from_bytes(self._iv, byteorder="big", signed=False)
        ctr = Counter.new(128, initial_value=initial_value)
        return AES.new(self._key, AES.MODE_CTR, counter=ctr)

    def encrypt(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        cipher = self._new_cipher()
        return cipher.encrypt(bytes(data))

    def decrypt(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        cipher = self._new_cipher()
        return cipher.decrypt(bytes(data))
