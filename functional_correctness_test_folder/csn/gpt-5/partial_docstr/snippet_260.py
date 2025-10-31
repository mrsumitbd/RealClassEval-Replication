import re
import fnmatch


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = str(spec)
        self.inclusive = bool(inclusive)
        self._regex = re.compile(fnmatch.translate(self.spec))

    def __str__(self):
        return f"{'+' if self.inclusive else '-'}{self.spec}"

    def matches(self, path):
        s = str(path)
        return self._regex.match(s) is not None
