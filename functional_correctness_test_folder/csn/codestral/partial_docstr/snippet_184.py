
class Encoder:

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        for char in s:
            if not (char.isalnum() or char.isspace()):
                return True
        return False

    def encode(self, s):
        encoded = []
        for char in s:
            if char.isalnum() or char.isspace():
                encoded.append(char)
            else:
                encoded.append(f"\\x{ord(char):02x}")
        return ''.join(encoded)

    def decode(self, s):
        decoded = []
        i = 0
        while i < len(s):
            if s[i] == '\\' and i + 3 < len(s) and s[i+1] == 'x':
                hex_code = s[i+2:i+4]
                decoded.append(chr(int(hex_code, 16)))
                i += 4
            else:
                decoded.append(s[i])
                i += 1
        return ''.join(decoded)
