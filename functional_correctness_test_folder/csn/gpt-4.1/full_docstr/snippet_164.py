
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
            return ''

        # Each diff is a tuple: (op, old_line_no, old_count, new_line_no, new_count, lines)
        # op: 'replace', 'delete', 'insert', 'equal'
        # lines: list of lines (with or without \n)
        # We'll assume self.diffs is a list of such tuples.

        result = []
        for diff in self.diffs:
            op, old_start, old_count, new_start, new_count, lines = diff
            # Convert to 1-based indices for GNU diff
            old_start_1 = old_start + 1
            new_start_1 = new_start + 1
            header = f"@@ -{old_start_1},{old_count} +{new_start_1},{new_count} @@"
            result.append(header)
            for line in lines:
                if op == 'equal':
                    result.append(' ' + line.rstrip('\n'))
                elif op == 'delete':
                    result.append('-' + line.rstrip('\n'))
                elif op == 'insert':
                    result.append('+' + line.rstrip('\n'))
                elif op == 'replace':
                    # For replace, lines is a list of tuples: (tag, line)
                    for tag, l in line:
                        if tag == 'delete':
                            result.append('-' + l.rstrip('\n'))
                        elif tag == 'insert':
                            result.append('+' + l.rstrip('\n'))
                        elif tag == 'equal':
                            result.append(' ' + l.rstrip('\n'))
            # Add a blank line between hunks
            result.append('')
        return '\n'.join(result).rstrip('\n')
