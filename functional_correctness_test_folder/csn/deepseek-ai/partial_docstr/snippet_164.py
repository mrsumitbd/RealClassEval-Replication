
class patch_obj:

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

        # Assuming the first diff has the old and new ranges
        old_start, old_len, new_start, new_len = self.diffs[0]
        header = f"@@ -{old_start + 1},{old_len} +{new_start + 1},{new_len} @@\n"
        return header
