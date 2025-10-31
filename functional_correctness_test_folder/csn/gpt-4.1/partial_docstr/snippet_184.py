
import urllib.parse


class Encoder:

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        # We'll consider "special characters" as anything not unreserved in URL encoding
        # Unreserved: A-Z a-z 0-9 - _ . ~
        for c in s:
            if not (c.isalnum() or c in '-_.~'):
                return True
        return False

    def encode(self, s):
        return urllib.parse.quote(s, safe='-_.~')

    def decode(self, s):
        return urllib.parse.unquote(s)
