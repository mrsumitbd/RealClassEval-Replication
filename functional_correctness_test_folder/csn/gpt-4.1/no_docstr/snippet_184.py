
class Encoder:

    def needsEncoding(self, s):
        # Needs encoding if contains non-alphanumeric characters
        return any(not c.isalnum() for c in s)

    def encode(self, s):
        # Encode non-alphanumeric characters as %XX (hex)
        res = []
        for c in s:
            if c.isalnum():
                res.append(c)
            else:
                res.append('%{:02X}'.format(ord(c)))
        return ''.join(res)

    def decode(self, s):
        # Decode %XX sequences back to characters
        import re

        def repl(match):
            return chr(int(match.group(1), 16))
        return re.sub(r'%([0-9A-Fa-f]{2})', repl, s)
