class WordArray:

    def __init__(self, bytes):
        if isinstance(bytes, (bytearray, memoryview)):
            data = bytes.tobytes() if hasattr(bytes, "tobytes") else bytes.__bytes__()
        elif isinstance(bytes, (bytes,)):
            data = bytes
        elif isinstance(bytes, (list, tuple)) and all(isinstance(b, int) and 0 <= b <= 255 for b in bytes):
            data = bytes.__class__(bytes)
            data = bytes(data) if not isinstance(data, (bytes,)) else data
        else:
            raise TypeError(
                "Expected bytes-like object or sequence of integers in range 0..255")
        self._bytes = data
        pad_len = (-len(self._bytes)) % 4
        self._padded = self._bytes + b"\x00" * pad_len if pad_len else self._bytes
        self._words = [
            int.from_bytes(self._padded[i:i+4], "big")
            for i in range(0, len(self._padded), 4)
        ]

    def __getitem__(self, key):
        if isinstance(key, slice):
            words = self._words[key]
            # Reconstruct bytes from selected words
            b = b"".join(w.to_bytes(4, "big") for w in words)
            return WordArray(b)
        if isinstance(key, int):
            return self._words[key]
        raise TypeError("Invalid argument type")

    def __len__(self):
        return len(self._words)
