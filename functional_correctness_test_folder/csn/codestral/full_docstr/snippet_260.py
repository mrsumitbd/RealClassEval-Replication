
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
        indicator = '+' if self.inclusive else '-'
        return f"{indicator} {self.spec}"

    def matches(self, path):
        '''Check this pattern against given `path`.'''
        return bool(self.regex.match(path))

    def _glob_to_regex(self, pattern):
        '''Convert a glob pattern to a regular expression.'''
        i, n = 0, len(pattern)
        res = ''
        while i < n:
            c = pattern[i]
            i += 1
            if c == '*':
                res += '.*'
            elif c == '?':
                res += '.'
            elif c == '[':
                j = i
                if j < n and pattern[j] == '!':
                    j += 1
                if j < n and pattern[j] == ']':
                    j += 1
                while j < n and pattern[j] != ']':
                    j += 1
                if j >= n:
                    res += '\\['
                else:
                    stuff = pattern[i:j].replace('\\', '\\\\')
                    i = j + 1
                    if stuff[0] == '!':
                        stuff = '^' + stuff[1:]
                    elif stuff[0] == '^':
                        stuff = '\\' + stuff
                    res += f'[{stuff}]'
            else:
                res += re.escape(c)
        return re.compile(res)
