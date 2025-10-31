
class Pattern:

    def __init__(self, spec, inclusive):
        self.spec = spec
        self.inclusive = inclusive
        # Convert spec to a regex pattern
        import re
        # Escape all regex special chars except * and ?

        def escape(s):
            return re.sub(r'([.+^${}()|\[\]\\])', r'\\\1', s)
        pat = ''
        i = 0
        while i < len(spec):
            if spec[i] == '*':
                # Check for **
                if i + 1 < len(spec) and spec[i+1] == '*':
                    pat += '.*'
                    i += 2
                else:
                    pat += '[^/]*'
                    i += 1
            elif spec[i] == '?':
                pat += '[^/]'
                i += 1
            else:
                pat += escape(spec[i])
                i += 1
        self._regex = re.compile('^' + pat + '$')

    def __str__(self):
        return f"{'+' if self.inclusive else '-'}:{self.spec}"

    def matches(self, path):
        return bool(self._regex.match(path))
