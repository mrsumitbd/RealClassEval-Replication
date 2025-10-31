
class NoHashContext:

    def __init__(self, data=None):
        self.data = data if data is not None else b''

    def update(self, data):
        self.data += data

    def digest(self):
        return self.data

    def hexdigest(self):
        return self.data.hex()
