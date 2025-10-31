class TorConfigType:
    def parse(self, s):
        """
        Parse the input string for a Tor configuration value.
        The default implementation simply strips surrounding whitespace.
        """
        if not isinstance(s, str):
            raise TypeError(
                f"Expected a string for parsing, got {type(s).__name__}")
        return s.strip()

    def validate(self, s, instance, name):
        """
        Validate that the parsed value is a non‑empty string.
        Raises ValueError if validation fails.
        """
        if not isinstance(s, str):
            raise ValueError(
                f"Attribute '{name}' must be a string, got {type(s).__name__}")
        if s == "":
            raise ValueError(f"Attribute '{name}' cannot be an empty string")
        # If the instance has a custom validation method for this attribute, call it
        validate_method = getattr(instance, f"validate_{name}", None)
        if callable(validate_method):
            validate_method(s)  # let the instance perform further checks
        return True
