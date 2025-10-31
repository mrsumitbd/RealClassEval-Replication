
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
        diff_str = ""
        for diff in self.diffs:
            diff_str += "@@ -{},{} +{},{} @@\n".format(
                diff[0][0]+1, diff[0][1], diff[1][0]+1, diff[1][1])
            for line in diff[2]:
                if line.startswith('-'):
                    diff_str += line + "\n"
                elif line.startswith('+'):
                    diff_str += line + "\n"
                else:
                    diff_str += " " + line + "\n"
        return diff_str
