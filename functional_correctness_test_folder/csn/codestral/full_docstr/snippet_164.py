
class patch_obj:
    '''Class representing one patch operation.'''

    def __init__(self):
        '''Initializes with an empty list of diffs.'''
        self.diffs = []

    def __str__(self):
        '''Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.
        Returns:
          The GNU diff string.
        '''
        if not self.diffs:
            return ""

        start_a, size_a, start_b, size_b = self.diffs[0]
        end_a = start_a + size_a - 1
        end_b = start_b + size_b - 1

        header = f"@@ -{start_a + 1},{size_a} +{start_b + 1},{size_b} @@\n"
        body = "\n".join(f"{line[0]}{line[1]}" for line in self.diffs)

        return header + body
