
import fnmatch
import re


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        self.regex = re.compile(fnmatch.translate(spec))

    def __str__(self):
        return f"{'Include' if self.inclusive else 'Exclude'} pattern: {self.spec}"

    def matches(self, path):
        return bool(self.regex.match(path))
