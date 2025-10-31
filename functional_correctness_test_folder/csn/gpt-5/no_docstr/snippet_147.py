class NoHashContext:

    def __init__(self, data=None):
        if data is not None:
            self.update(data)

    def update(self, data):
        # Intentionally does nothing; placeholder for hash-like interface
        return None

    def digest(self):
        return b""

    def hexdigest(self):
        return ""
