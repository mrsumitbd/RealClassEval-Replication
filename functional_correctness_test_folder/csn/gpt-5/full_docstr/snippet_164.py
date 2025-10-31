class patch_obj:
    '''Class representing one patch operation.'''

    def __init__(self):
        '''Initializes with an empty list of diffs.'''
        self.diffs = []
        self.start1 = 0
        self.start2 = 0
        self.length1 = 0
        self.length2 = 0

    def __str__(self):
        '''Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.
        Returns:
          The GNU diff string.
        '''
        from urllib.parse import quote

        def coord(start, length):
            if length == 0:
                return f"{start},0"
            if length == 1:
                return f"{start + 1}"
            return f"{start + 1},{length}"

        header = f"@@ -{coord(self.start1, self.length1)} +{coord(self.start2, self.length2)} @@\n"

        # Map operations to their prefixes.
        def op_prefix(op):
            if op in (-1, 'delete', 'DELETE', '-'):
                return '-'
            if op in (1, 'insert', 'INSERT', '+'):
                return '+'
            return ' '

        # Encode text similar to diff-match-patch: percent-encode, but keep spaces as spaces for readability.
        def encode_text(t):
            enc = quote(t, safe="~!*()'")
            return enc.replace('%20', ' ')

        lines = []
        lines.append(header)
        for op, text in self.diffs:
            lines.append(op_prefix(op) + encode_text(text) + "\n")
        return ''.join(lines)
