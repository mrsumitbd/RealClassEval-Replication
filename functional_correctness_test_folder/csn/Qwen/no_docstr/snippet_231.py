
class WordArray:

    def __init__(self, bytes):
        self.words = [int.from_bytes(bytes[i:i+4], byteorder='little')
                      for i in range(0, len(bytes), 4)]

    def __getitem__(self, key):
        return self.words[key]

    def __len__(self):
        return len(self.words)
