
import base64


class Encoder:

    def needsEncoding(self, s):
        """Check if a string contains non-ASCII characters."""
        return not all(ord(c) < 128 for c in s)

    def encode(self, s):
        """Encode a string using Base64."""
        return base64.b64encode(s.encode('utf-8')).decode('utf-8')

    def decode(self, s):
        """Decode a Base64 encoded string."""
        return base64.b64decode(s.encode('utf-8')).decode('utf-8')
