
import re
import fnmatch


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        # fnmatch.translate returns a regex string that matches the whole string
        self._regex = re.compile(fnmatch.translate(spec))

    def __str__(self):
        return f"{'INCLUDE' if self.inclusive else 'EXCLUDE'}: {self.spec}"

    def matches(self, path):
        '''Return True if the given path matches this pattern.'''
        return bool(self._regex.match(path))
