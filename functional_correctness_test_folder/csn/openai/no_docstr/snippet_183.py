
import hashlib


class Reader:
    def __init__(self, options):
        """
        Initialize the Reader with a dictionary of options.
        Supported options:
            - prefix: string to prepend to the name
            - suffix: string to append to the name
            - separator: string used between name and x when hashing
            - hash: boolean, if True use a SHA-256 hash of the name and x
        """
        if not isinstance(options, dict):
            raise TypeError("options must be a dictionary")
        self.options = options

    def mangle(self, name, x):
        """
        Return a mangled version of `name` based on the options.
        If the 'hash' option is True, return a SHA-256 hex digest of
        the concatenation of name, separator, and x (converted to string).
        Otherwise, return the name with optional prefix and suffix.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        # Handle hashing first
        if self.options.get("hash"):
            separator = self.options.get("separator", "_")
            to_hash = f"{name}{separator}{x}"
            return hashlib.sha256(to_hash.encode("utf-8")).hexdigest()

        # Build the mangled name with prefix/suffix
        prefix = self.options.get("prefix", "")
        suffix = self.options.get("suffix", "")
        return f"{prefix}{name}{suffix}"
