import urllib.parse

class patch_obj:
    """Class representing one patch operation."""

    def __init__(self):
        """Initializes with an empty list of diffs."""
        self.diffs = []
        self.start1 = None
        self.start2 = None
        self.length1 = 0
        self.length2 = 0

    def __str__(self):
        """Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.

        Returns:
          The GNU diff string.
        """
        if self.length1 == 0:
            coords1 = str(self.start1) + ',0'
        elif self.length1 == 1:
            coords1 = str(self.start1 + 1)
        else:
            coords1 = str(self.start1 + 1) + ',' + str(self.length1)
        if self.length2 == 0:
            coords2 = str(self.start2) + ',0'
        elif self.length2 == 1:
            coords2 = str(self.start2 + 1)
        else:
            coords2 = str(self.start2 + 1) + ',' + str(self.length2)
        text = ['@@ -', coords1, ' +', coords2, ' @@\n']
        for op, data in self.diffs:
            if op == diff_match_patch.DIFF_INSERT:
                text.append('+')
            elif op == diff_match_patch.DIFF_DELETE:
                text.append('-')
            elif op == diff_match_patch.DIFF_EQUAL:
                text.append(' ')
            data = data.encode('utf-8')
            text.append(urllib.parse.quote(data, "!~*'();/?:@&=+$,# ") + '\n')
        return ''.join(text)