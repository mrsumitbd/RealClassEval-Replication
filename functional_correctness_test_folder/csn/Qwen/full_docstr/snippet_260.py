
import re


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        self.regex = self._glob_to_regex(spec)

    def __str__(self):
        '''Return inclusiveness indicator and original glob pattern.'''
        return f"{'+' if self.inclusive else '-'}{self.spec}"

    def matches(self, path):
        '''Check this pattern against given `path`.'''
        return bool(self.regex.match(path))

    def _glob_to_regex(self, glob):
        '''Convert a glob pattern to a regex pattern.'''
        regex = re.escape(glob)
        regex = regex.replace(r'\*', '.*')
        regex = regex.replace(r'\?', '.')
        return re.compile(f"^{regex}$")
