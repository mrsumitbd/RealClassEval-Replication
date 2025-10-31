
import re


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        self.regex = self._glob_to_regex(spec)

    def __str__(self):
        return f"Pattern(spec={self.spec}, inclusive={self.inclusive})"

    def matches(self, path):
        return bool(self.regex.match(path))

    def _glob_to_regex(self, pattern):
        regex = pattern
        regex = regex.replace('.', r'\.')
        regex = regex.replace('?', '.')
        regex = regex.replace('**', '.*')
        regex = regex.replace('*', '[^/]*')
        regex = regex.replace('+', r'\+')
        regex = regex.replace('(', r'\(')
        regex = regex.replace(')', r'\)')
        regex = regex.replace('{', r'\{')
        regex = regex.replace('}', r'\}')
        regex = regex.replace('[', r'\[')
        regex = regex.replace(']', r'\]')
        regex = regex.replace('^', r'\^')
        regex = regex.replace('$', r'\$')
        regex = regex.replace('|', r'\|')
        return re.compile(f'^{regex}$')
