
class Encoder:

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        return any(not c.isalnum() and not c.isspace() for c in s)

    def encode(self, s):
        '''
        Encode the string by replacing special characters with their ASCII values.
        @param s: A string to encode.
        @type s: str
        @return: Encoded string.
        @rtype: str
        '''
        return ''.join(str(ord(c)) if not c.isalnum() and not c.isspace() else c for c in s)

    def decode(self, s):
        '''
        Decode the string by converting ASCII values back to their original characters.
        @param s: A string to decode.
        @type s: str
        @return: Decoded string.
        @rtype: str
        '''
        decoded_chars = []
        i = 0
        while i < len(s):
            if s[i].isdigit():
                num = s[i]
                while i + 1 < len(s) and s[i + 1].isdigit():
                    i += 1
                    num += s[i]
                decoded_chars.append(chr(int(num)))
            else:
                decoded_chars.append(s[i])
            i += 1
        return ''.join(decoded_chars)
