
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

    # Mapping of characters to their XML entity encodings
    encodings = [
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('"', '&quot;'),
        ("'", '&apos;')
    ]

    # Reverse mapping for decoding
    decodings = [(v, k) for k, v in encodings]

    # List of characters that need encoding
    special = [k for k, _ in encodings]

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        return any(ch in s for ch in self.special)

    def encode(self, s):
        '''
        Encode special characters found in string I{s}.
        @param s: A string to encode.
        @type s: str
        @return: The encoded string.
        @rtype: str
        '''
        if not s:
            return s
        result = s
        for ch, enc in self.encodings:
            result = result.replace(ch, enc)
        return result

    def decode(self, s):
        '''
        Decode special characters encodings found in string I{s}.
        @param s: A string to decode.
        @type s: str
        @return: The decoded string.
        @rtype: str
        '''
        if not s:
            return s
        result = s
        for enc, ch in self.decodings:
            result = result.replace(enc, ch)
        return result
