from io import BufferedReader

class NotNullWrapper(BufferedReader):
    """BufferedReader which removes NUL (`\x00`) from source stream"""

    def read(self, n):
        return super().read(n).replace(b'\x00', b'')

    def readline(self):
        return super().readline().replace(b'\x00', b'')