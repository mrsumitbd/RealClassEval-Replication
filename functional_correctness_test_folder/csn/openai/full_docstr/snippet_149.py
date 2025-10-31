
class TorConfigType:
    """
    Base class for all configuration types, which function as parsers
    and un-parsers.
    """

    def parse(self, s):
        """
        Given the string s, this should return a parsed representation of it.
        The default implementation simply returns the string unchanged.
        """
        return s

    def validate(self, s, instance, name):
        """
        If s is not a valid type for this object, an exception should
        be thrown. The validated object should be returned.
        The default implementation checks that the instance is a string.
        """
        if not isinstance(instance, str):
            raise ValueError(
                f"Invalid type for '{name}': expected str, got {type(instance).__name__}"
            )
        return instance
