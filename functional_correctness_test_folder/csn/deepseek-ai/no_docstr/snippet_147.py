
class NoHashContext:

    def __init__(self, data=None):
        self._data = bytearray()
        if data is not None:
            self.update(data)

    def update(self, data):
        if isinstance(data, (bytes, bytearray)):
            self._data.extend(data)
        elif isinstance(data, str):
            self._data.extend(data.encode('utf-8'))
        else:
            raise TypeError("Data must be bytes, bytearray, or str")

    def digest(self):
        return bytes(self._data)

    def hexdigest(self):
        return self.digest().hex()
