
import hashlib


class NoHashContext:

    def __init__(self, data=None):
        self.md5_hash = hashlib.md5()
        if data is not None:
            self.update(data)

    def update(self, data):
        self.md5_hash.update(data)

    def digest(self):
        return self.md5_hash.digest()

    def hexdigest(self):
        return self.md5_hash.hexdigest()
