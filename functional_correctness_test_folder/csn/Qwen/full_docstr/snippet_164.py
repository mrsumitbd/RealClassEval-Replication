
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

        lines = []
        old_start, old_count = self.diffs[0][0], 0
        new_start, new_count = self.diffs[0][1], 0

        for diff in self.diffs:
            old_line, new_line, change_type = diff
            if change_type == 'delete':
                old_count += 1
            if change_type == 'insert':
                new_count += 1
            if change_type == 'replace':
                old_count += 1
                new_count += 1

        lines.append(
            f"@@ -{old_start + 1},{old_count} +{new_start + 1},{new_count} @@")
        for diff in self.diffs:
            old_line, new_line, change_type = diff
            if change_type == 'delete':
                lines.append(f"-{old_line}")
            elif change_type == 'insert':
                lines.append(f"+{new_line}")
            elif change_type == 'replace':
                lines.append(f"-{old_line}")
                lines.append(f"+{new_line}")

        return "\n".join(lines)
