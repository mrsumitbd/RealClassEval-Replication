
class patch_obj:
    '''Class representing one patch operation.'''

    def __init__(self):
        '''Initializes with an empty list of diffs.'''
        self.diffs = []

    def add_diff(self, old_line, new_line, line_content):
        '''Adds a diff to the list of diffs.

        Args:
          old_line (int): The line number in the old file.
          new_line (int): The line number in the new file.
          line_content (str): The content of the line with a prefix indicating the type of diff.
        '''
        self.diffs.append((old_line, new_line, line_content))

    def __str__(self):
        '''Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.
        Returns:
          The GNU diff string.
        '''
        if not self.diffs:
            return ''

        old_start = min(old_line for old_line, _,
                        _ in self.diffs if old_line is not None)
        new_start = min(new_line for _, new_line,
                        _ in self.diffs if new_line is not None)

        old_count = sum(
            1 for old_line, _, line_content in self.diffs if old_line is not None and line_content.startswith('-'))
        new_count = sum(
            1 for _, new_line, line_content in self.diffs if new_line is not None and line_content.startswith('+'))

        if old_count == 0:
            old_count = 1
        if new_count == 0:
            new_count = 1

        header = f'@@ -{old_start},{old_count} +{new_start},{new_count} @@\n'

        diff_str = header
        for _, _, line_content in self.diffs:
            diff_str += line_content + '\n'

        return diff_str.rstrip()
