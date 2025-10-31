
import re
import os.path


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        self.regex = self._glob_to_regex(spec)

    def _glob_to_regex(self, pattern):
        # Escape special regex characters except '*'
        regex = re.escape(pattern)
        # Replace escaped '*' with '.*' for regex wildcard
        regex = regex.replace(r'\*', '.*')
        # Ensure the pattern matches the entire string
        regex = f'^{regex}$'
        return re.compile(regex)

    def __str__(self):
        prefix = '+' if self.inclusive else '-'
        return f'{prefix}{self.spec}'

    def matches(self, path):
        return bool(self.regex.match(path))
