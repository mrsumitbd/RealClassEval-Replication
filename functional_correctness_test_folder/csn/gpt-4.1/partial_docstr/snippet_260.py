
import re
import fnmatch


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        # Convert glob to regex
        regex = fnmatch.translate(spec)
        self._regex = re.compile(regex)

    def __str__(self):
        return f"{'+' if self.inclusive else '-'}:{self.spec}"

    def matches(self, path):
        return self._regex.match(path) is not None
