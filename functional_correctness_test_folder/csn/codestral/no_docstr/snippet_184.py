
class Encoder:

    def needsEncoding(self, s):
        return any(ord(char) > 127 for char in s)

    def encode(self, s):
        if not self.needsEncoding(s):
            return s
        return s.encode('utf-8')

    def decode(self, s):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s
