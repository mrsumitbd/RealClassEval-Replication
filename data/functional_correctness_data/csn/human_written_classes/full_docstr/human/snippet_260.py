class Pattern:
    """A single pattern for either inclusion or exclusion."""

    def __init__(self, spec, inclusive):
        """Create regex-based pattern matcher from glob `spec`."""
        self.compiled = compile_glob(spec.rstrip('/'))
        self.inclusive = inclusive
        self.is_dir = spec.endswith('/')

    def __str__(self):
        """Return inclusiveness indicator and original glob pattern."""
        return ('+' if self.inclusive else '-') + self.compiled.pattern

    def matches(self, path):
        """Check this pattern against given `path`."""
        return bool(self.compiled.match(path))