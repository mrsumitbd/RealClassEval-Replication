import re
import fnmatch


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = bool(inclusive)
        self._regex = re.compile(fnmatch.translate(spec))

    def __str__(self):
        '''Return inclusiveness indicator and original glob pattern.'''
        return f"{'+' if self.inclusive else '-'}{self.spec}"

    def matches(self, path):
        '''Check this pattern against given `path`.'''
        return self._regex.match(path) is not None
