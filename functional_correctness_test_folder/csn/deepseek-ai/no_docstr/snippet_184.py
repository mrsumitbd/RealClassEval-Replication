
class Encoder:

    def needsEncoding(self, s):
        return any(ord(c) > 127 for c in s)

    def encode(self, s):
        return s.encode('utf-8').hex()

    def decode(self, s):
        return bytes.fromhex(s).decode('utf-8')
