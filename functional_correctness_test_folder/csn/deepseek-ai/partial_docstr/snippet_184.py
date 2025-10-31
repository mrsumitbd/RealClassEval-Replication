
class Encoder:

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        return any(not c.isalnum() for c in s)

    def encode(self, s):
        import urllib.parse
        return urllib.parse.quote(s)

    def decode(self, s):
        import urllib.parse
        return urllib.parse.unquote(s)
