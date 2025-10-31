class patch_obj:

    def __init__(self):
        '''Initializes with an empty list of diffs.'''
        self.diffs = []
        self.start1 = 0
        self.start2 = 0
        self.length1 = 0
        self.length2 = 0

    def __str__(self):
        '''Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.
        Returns:
          The GNU diff string.
        '''
        if self.length1 == 0:
            coords1 = f'{self.start1 + 1},0'
        elif self.length1 == 1:
            coords1 = f'{self.start1 + 1}'
        else:
            coords1 = f'{self.start1 + 1},{self.length1}'

        if self.length2 == 0:
            coords2 = f'{self.start2 + 1},0'
        elif self.length2 == 1:
            coords2 = f'{self.start2 + 1}'
        else:
            coords2 = f'{self.start2 + 1},{self.length2}'

        text = [f'@@ -{coords1} +{coords2} @@\n']
        for (op, data) in self.diffs:
            safe = data.replace('%', '%25').replace(
                '\n', '%0A').replace('\r', '%0D')
            if op == 1:
                text.append('+' + safe + '\n')
            elif op == -1:
                text.append('-' + safe + '\n')
            else:
                text.append(' ' + safe + '\n')
        return ''.join(text)
