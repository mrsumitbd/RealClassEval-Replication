
import fnmatch


class Pattern:

    def __init__(self, spec, inclusive):
        self.spec = spec
        self.inclusive = inclusive

    def __str__(self):
        return f"{'Include' if self.inclusive else 'Exclude'} pattern '{self.spec}'"

    def matches(self, path):
        return fnmatch.fnmatch(path, self.spec) == self.inclusive
