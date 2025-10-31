class AES_GCM_Mechanism:

    def __init__(self, iv, aad, tagBits):
        # Normalize and validate IV
        if iv is None:
            raise ValueError("iv must not be None")
        try:
            self.iv = bytes(iv)
        except Exception as e:
            raise TypeError("iv must be bytes-like") from e
        if len(self.iv) == 0:
            raise ValueError("iv must not be empty")

        # Normalize and validate AAD
        if aad is None:
            self.aad = b""
        else:
            try:
                self.aad = bytes(aad)
            except Exception as e:
                raise TypeError("aad must be bytes-like or None") from e

        # Validate tagBits
        if not isinstance(tagBits, int):
            raise TypeError("tagBits must be an integer")
        if not (32 <= tagBits <= 128) or (tagBits % 8 != 0):
            raise ValueError(
                "tagBits must be between 32 and 128 (inclusive) and a multiple of 8")
        self.tagBits = tagBits

    def to_native(self):
        return {
            "iv": self.iv,
            "aad": self.aad,
            "tagBits": self.tagBits,
        }
