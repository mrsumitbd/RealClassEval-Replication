
class Pattern:

    def __init__(self, spec, inclusive):
        self.spec = spec
        self.inclusive = inclusive

    def __str__(self):
        return f"Pattern(spec={self.spec}, inclusive={self.inclusive})"

    def matches(self, path):
        if self.inclusive:
            return path.startswith(self.spec)
        else:
            return not path.startswith(self.spec)
