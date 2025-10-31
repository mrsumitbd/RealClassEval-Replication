
class WordArray:

    def __init__(self, bytes):
        self.bytes = bytes

    def __getitem__(self, key):
        return self.bytes[key]

    def __len__(self):
        return len(self.bytes)
