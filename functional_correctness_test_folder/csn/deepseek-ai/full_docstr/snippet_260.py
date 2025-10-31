
import re
import os


class Pattern:
    '''A single pattern for either inclusion or exclusion.'''

    def __init__(self, spec, inclusive):
        '''Create regex-based pattern matcher from glob `spec`.'''
        self.spec = spec
        self.inclusive = inclusive
        self.regex = self._glob_to_regex(spec)

    def __str__(self):
        '''Return inclusiveness indicator and original glob pattern.'''
        prefix = '+' if self.inclusive else '-'
        return f"{prefix}{self.spec}"

    def matches(self, path):
        '''Check this pattern against given `path`.'''
        return self.regex.fullmatch(path) is not None

    def _glob_to_regex(self, pattern):
        '''Convert a glob pattern to a compiled regex.'''
        regex = []
        i = 0
        n = len(pattern)
        while i < n:
            c = pattern[i]
            i += 1
            if c == '*':
                if i < n and pattern[i] == '*':
                    i += 1
                    if i < n and pattern[i] == '/':
                        i += 1
                        regex.append('(?:.*/)?')
                    else:
                        regex.append('.*')
                else:
                    regex.append('[^/]*')
            elif c == '?':
                regex.append('[^/]')
            elif c == '[':
                j = i
                if j < n and pattern[j] == '!':
                    j += 1
                if j < n and pattern[j] == ']':
                    j += 1
                while j < n and pattern[j] != ']':
                    j += 1
                if j >= n:
                    regex.append('\\[')
                else:
                    part = pattern[i-1:j+1]
                    regex.append(part)
                    i = j + 1
            else:
                regex.append(re.escape(c))
        regex = ''.join(regex)
        regex = f'^{regex}$'
        return re.compile(regex)
