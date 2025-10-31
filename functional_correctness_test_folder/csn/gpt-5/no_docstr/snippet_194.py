class EXTRACT_KEY_FROM_KEY_Mechanism:

    def __init__(self, extractParams):
        self.extract_params = extractParams

    def to_native(self):
        p = self.extract_params
        if p is None:
            return b""
        if isinstance(p, (bytes, bytearray, memoryview)):
            return bytes(p)
        if isinstance(p, int):
            import struct
            return struct.pack("=I", p)
        if isinstance(p, str):
            return p.encode("utf-8")
        try:
            return bytes(p)
        except Exception as e:
            raise TypeError(
                f"Unsupported type for extractParams: {type(p)!r}") from e
