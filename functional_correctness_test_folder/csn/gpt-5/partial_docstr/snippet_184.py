class Encoder:

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        if s is None:
            return False
        if not isinstance(s, str):
            s = str(s)
        specials = {'&', '<', '>', '"', "'"}
        return any(ch in specials for ch in s)

    def encode(self, s):
        if s is None:
            return None
        if not isinstance(s, str):
            s = str(s)
        import re
        # Encode & only if it does not start an existing entity
        s = re.sub(r'&(?!(?:#\d+|#x[0-9a-fA-F]+|\w+);)', '&amp;', s)
        s = s.replace('<', '&lt;').replace('>', '&gt;')
        s = s.replace('"', '&quot;').replace("'", '&apos;')
        return s

    def decode(self, s):
        if s is None:
            return None
        if not isinstance(s, str):
            s = str(s)
        # Decode named entities
        s = s.replace('&lt;', '<').replace('&gt;', '>')
        s = s.replace('&quot;', '"').replace('&apos;', "'")
        # Decode numeric entities (decimal and hex)
        import re

        def repl_dec(m):
            text = m.group(0)
            try:
                cp = int(m.group(1), 10)
                return chr(cp)
            except Exception:
                return text

        def repl_hex(m):
            text = m.group(0)
            try:
                cp = int(m.group(1), 16)
                return chr(cp)
            except Exception:
                return text

        s = re.sub(r'&#(\d+);', repl_dec, s)
        s = re.sub(r'&#[xX]([0-9a-fA-F]+);', repl_hex, s)
        # Finally decode &amp; (do this last to avoid interfering with other entities)
        s = s.replace('&amp;', '&')
        return s
