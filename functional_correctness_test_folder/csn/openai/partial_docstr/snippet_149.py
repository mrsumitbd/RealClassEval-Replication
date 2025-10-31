class TorConfigType:
    """
    Base class for all configuration types, which function as parsers
    and un-parsers.
    """

    def parse(self, s):
        """
        Parse the input string `s` into a Python object.
        The default implementation simply returns the string unchanged.
        Subclasses should override this method to provide custom parsing logic.
        """
        if not isinstance(s, str):
            raise TypeError(
                f"Expected a string for parsing, got {type(s).__name__}")
        return s

    def validate(self, s, instance, name):
        """
        Validate that the parsed `instance` is acceptable for the configuration
        identified by `name`. The default implementation performs basic checks
        and returns True if validation passes.
        Subclasses may override this method to enforce stricter rules.
        """
        if not isinstance(s, str):
            raise TypeError(
                f"Expected a string for validation, got {type(s).__name__}")
        if instance is None:
            raise ValueError(f"Instance for '{name}' cannot be None")
        return True
