
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

        lines = []
        for diff in self.diffs:
            old_start, old_count, new_start, new_count, changes = diff
            lines.append(
                f"@@ -{old_start},{old_count} +{new_start},{new_count} @@")
            lines.extend(changes)

        return "\n".join(lines)
