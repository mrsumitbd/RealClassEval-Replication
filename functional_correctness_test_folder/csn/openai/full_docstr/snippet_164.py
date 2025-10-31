
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
        lines = []
        for diff in self.diffs:
            # Support both dict and tuple/list diff representations
            if isinstance(diff, dict):
                old_start = diff.get('old_start', 0) + 1
                old_count = diff.get('old_count', 0)
                new_start = diff.get('new_start', 0) + 1
                new_count = diff.get('new_count', 0)
                diff_lines = diff.get('lines', [])
            else:
                # Assume tuple/list: (old_start, old_count, new_start, new_count, lines)
                old_start, old_count, new_start, new_count, diff_lines = diff
                old_start += 1
                new_start += 1

            header = f"@@ -{old_start},{old_count} +{new_start},{new_count} @@"
            lines.append(header)
            lines.extend(diff_lines)

        return "\n".join(lines)
