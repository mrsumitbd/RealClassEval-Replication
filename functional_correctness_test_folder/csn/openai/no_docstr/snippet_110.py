
class Enum:
    """
    A simple enumeration base class.

    Example usage:

        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        print(Color.iteritems())   # [('RED', 1), ('GREEN', 2), ('BLUE', 3)]
        print(Color.RED)           # <Color RED>
    """

    def __repr__(self):
        """
        Return a readable representation of the enum value.
        If the instance has `_name` and `_value` attributes (created by
        accessing an enum member), show them; otherwise fall back to
        the default string conversion.
        """
        if hasattr(self, "_name") and hasattr(self, "_value"):
            return f"<{self.__class__.__name__} {self._name}>"
        return f"<{self.__class__.__name__} {self!s}>"

    @classmethod
    def iteritems(cls):
        """
        Return a list of (name, value) tuples for all public
        attributes of the enum class that are not callables.
        """
        return [
            (name, value)
            for name, value in vars(cls).items()
            if not name.startswith("_") and not callable(value)
        ]
