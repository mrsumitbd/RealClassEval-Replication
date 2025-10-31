
class TorConfigType:
    """
    A class representing a Tor configuration type.
    """

    def parse(self, s):
        """
        Parse a string into a valid configuration value.

        Args:
            s (str): The string to be parsed.

        Returns:
            The parsed configuration value.
        """
        raise NotImplementedError("Subclasses must implement the parse method")

    def validate(self, s, instance, name):
        """
        Validate a configuration value.

        Args:
            s: The configuration value to be validated.
            instance: The instance that the configuration value belongs to.
            name (str): The name of the configuration attribute.

        Raises:
            ValueError: If the configuration value is invalid.
        """
        try:
            self.parse(s)
        except Exception as e:
            raise ValueError(f"Invalid value for {name}: {s}") from e
