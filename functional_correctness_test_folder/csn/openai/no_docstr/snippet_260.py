
import fnmatch


class Pattern:
    """
    A simple pattern matcher that supports glob-style patterns.
    The `inclusive` flag determines whether the pattern is used to include
    or exclude paths.
    """

    def __init__(self, spec, inclusive):
        """
        Parameters
        ----------
        spec : str
            The glob pattern to match against.
        inclusive : bool
            If True, `matches` returns True when the path matches the pattern.
            If False, `matches` returns True when the path does NOT match the pattern.
        """
        self.spec = spec
        self.inclusive = inclusive

    def __str__(self):
        return f"Pattern(spec={self.spec!r}, inclusive={self.inclusive})"

    def matches(self, path):
        """
        Check if the given path matches the pattern.

        Parameters
        ----------
        path : str
            The path to test against the pattern.

        Returns
        -------
        bool
            True if the path matches the pattern according to the inclusive flag.
        """
        matched = fnmatch.fnmatch(path, self.spec)
        return matched if self.inclusive else not matched
