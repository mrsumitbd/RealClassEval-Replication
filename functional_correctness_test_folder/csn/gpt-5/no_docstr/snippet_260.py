class Pattern:

    def __init__(self, spec, inclusive):
        import re
        import fnmatch
        if not isinstance(spec, str):
            raise TypeError("spec must be a string")
        if not isinstance(inclusive, bool):
            raise TypeError("inclusive must be a boolean")
        self.spec = spec
        self.inclusive = inclusive
        # Precompile regex from glob-like spec
        self._regex = re.compile(fnmatch.translate(spec))

    def __str__(self):
        sign = "+" if self.inclusive else "-"
        return f"{sign} {self.spec}"

    def matches(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        # fnmatch.translate produces a regex that matches the entire string
        matched = self._regex.fullmatch(path) is not None
        if not matched:
            return False
        return self.inclusive
