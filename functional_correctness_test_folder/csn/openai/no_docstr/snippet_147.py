class NoHashContext:
    def __init__(self, data=None):
        self._data = b''
        if data is not None:
            self.update(data)

    def update(self, data):
        if isinstance(data, (bytes, bytearray, memoryview)):
            self._data += bytes(data)
        elif isinstance(data, str):
            self._data += data.encode('utf-8')
        else:
            raise TypeError(f"Unsupported data type: {type(data).__name__}")

    def digest(self):
        return self._data

    def hexdigest(self):
        return self._data.hex()
