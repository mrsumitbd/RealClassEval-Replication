
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
        result = []
        for diff in self.diffs:
            # Each diff is a dict: {'old_start': int, 'old_len': int, 'new_start': int, 'new_len': int, 'lines': list of (tag, line)}
            old_start = diff['old_start'] + 1  # 1-based
            old_len = diff['old_len']
            new_start = diff['new_start'] + 1  # 1-based
            new_len = diff['new_len']
            header = f"@@ -{old_start},{old_len} +{new_start},{new_len} @@"
            result.append(header)
            for tag, line in diff['lines']:
                if tag == ' ':
                    result.append(f" {line}")
                elif tag == '-':
                    result.append(f"-{line}")
                elif tag == '+':
                    result.append(f"+{line}")
        return '\n'.join(result)
