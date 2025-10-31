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

    # Class-level mappings for XML special characters
    encodings = [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ('"', "&quot;"),
        ("'", "&apos;"),
    ]

    decodings = [
        ("&amp;", "&"),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&quot;", '"'),
        ("&apos;", "'"),
    ]

    special = [c for c, _ in encodings]

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        if not s:
            return False
        for ch in s:
            if ch in self.special:
                return True
        return False

    def encode(self, s):
        '''
        Encode special characters found in string I{s}.
        @param s: A string to encode.
        @type s: str
        @return: The encoded string.
        @rtype: str
        '''
        if s is None or s == "":
            return s
        # Encode by scanning to avoid double-encoding
        mapping = dict(self.encodings)
        out = []
        for ch in s:
            out.append(mapping.get(ch, ch))
        return "".join(out)

    def decode(self, s):
        '''
        Decode special characters encodings found in string I{s}.
        @param s: A string to decode.
        @type s: str
        @return: The decoded string.
        @rtype: str
        '''
        if s is None or s == "":
            return s
        # Iteratively replace to handle nested encodings like &amp;lt;
        changed = True
        while changed:
            changed = False
            for entity, ch in self.decodings:
                new_s = s.replace(entity, ch)
                if new_s != s:
                    changed = True
                    s = new_s
        return s
