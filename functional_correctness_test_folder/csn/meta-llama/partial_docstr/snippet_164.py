
class patch_obj:

    def __init__(self):
        '''Initializes with an empty list of diffs.'''
        self.diffs = []

    def add_diff(self, old_start, old_length, new_start, new_length, lines):
        '''Adds a diff to the list of diffs.

        Args:
          old_start (int): The 0-based start index of the old file.
          old_length (int): The length of the old file section.
          new_start (int): The 0-based start index of the new file.
          new_length (int): The length of the new file section.
          lines (list): A list of strings representing the diff lines.
        '''
        self.diffs.append({
            'old_start': old_start,
            'old_length': old_length,
            'new_start': new_start,
            'new_length': new_length,
            'lines': lines
        })

    def __str__(self):
        '''Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.
        Returns:
          The GNU diff string.
        '''
        diff_str = ''
        for diff in self.diffs:
            old_start = diff['old_start'] + 1
            old_length = diff['old_length']
            new_start = diff['new_start'] + 1
            new_length = diff['new_length']
            lines = diff['lines']
            diff_str += f'@@ -{old_start},{old_length} +{new_start},{new_length} @@\n'
            for line in lines:
                diff_str += line + '\n'
        return diff_str.rstrip()  # Remove trailing newline


# Example usage:
if __name__ == "__main__":
    patch = patch_obj()
    patch.add_diff(0, 2, 0, 3, ['-line1', '-line2',
                   '+line1', '+line2', '+line3'])
    print(patch)
