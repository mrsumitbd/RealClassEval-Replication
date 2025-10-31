
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
        coords1 = f"-{self.start1 + 1}"
        if self.length1 != 1:
            coords1 += f",{self.length1}"
        coords2 = f"+{self.start2 + 1}"
        if self.length2 != 1:
            coords2 += f",{self.length2}"
        header = f"@@ {coords1} {coords2} @@\n"
        return header + "".join(str(diff) for diff in self.diffs)
