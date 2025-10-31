
class Encoder:
    '''
    An XML special character encoder/decoder.
    @cvar encodings: A mapping of special characters encoding.
    @type encodings: [(str,str)]
    @cvar decodings: A mapping of special characters decoding.
    @type decodings: [(str,str)]
    @cvar special: A list of special characters
    @type special: [char]
    '''

    encodings = [
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&apos;')
    ]
    decodings = [
        ('&amp;', '&'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&quot;', '"'),
        ('&apos;', "'")
    ]
    special = ['&', '<', '>', '"', "'"]

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        return any(c in s for c in self.special)

    def encode(self, s):
        '''
        Encode special characters found in string I{s}.
        @param s: A string to encode.
        @type s: str
        @return: The encoded string.
        @rtype: str
        '''
        for char, enc in self.encodings:
            s = s.replace(char, enc)
        return s

    def decode(self, s):
        '''
        Decode special characters encodings found in string I{s}.
        @param s: A string to decode.
        @type s: str
        @return: The decoded string.
        @rtype: str
        '''
        for enc, char in self.decodings:
            s = s.replace(enc, char)
        return s
