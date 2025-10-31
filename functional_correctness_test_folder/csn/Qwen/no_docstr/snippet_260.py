
import fnmatch


class Pattern:

    def __init__(self, spec, inclusive):
        self.spec = spec
        self.inclusive = inclusive

    def __str__(self):
        return f"Pattern(spec='{self.spec}', inclusive={self.inclusive})"

    def matches(self, path):
        if self.inclusive:
            return fnmatch.fnmatch(path, self.spec)
        else:
            return not fnmatch.fnmatch(path, self.spec)
