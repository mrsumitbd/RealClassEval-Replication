
import re


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.inclusive = inclusive
        self.pattern = re.compile(fnmatch.translate(spec))

    def __str__(self):
        return f"Pattern(spec={self.pattern.pattern}, inclusive={self.inclusive})"

    def matches(self, path):
        return bool(self.pattern.match(path))
