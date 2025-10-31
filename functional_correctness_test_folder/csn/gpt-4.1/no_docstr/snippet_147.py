
class NoHashContext:

    def __init__(self, data=None):
        self._data = b""
        if data is not None:
            self.update(data)

    def update(self, data):
        if isinstance(data, str):
            data = data.encode()
        self._data += data

    def digest(self):
        return self._data

    def hexdigest(self):
        return self._data.hex()
