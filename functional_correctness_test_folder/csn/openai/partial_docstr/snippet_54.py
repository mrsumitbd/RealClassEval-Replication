class Enum:
    def __init__(self, *args, **kwargs):
        """
        Create an enumeration.

        Positional arguments are treated as names and are automatically assigned
        integer values starting from 0. Keyword arguments allow explicit
        mapping of names to integer values.

        Example:
            Color = Enum('RED', 'GREEN', 'BLUE')
            Status = Enum(OK=0, ERROR=1, UNKNOWN=2)
        """
        self._value_to_name = {}
        self._name_to_value = {}

        # Handle positional names
        for i, name in enumerate(args):
            if not isinstance(name, str):
                raise TypeError(
                    f"Enum name must be a string, got {type(name).__name__}")
            if name in self._name_to_value:
                raise ValueError(f"Duplicate enum name: {name}")
            if i in self._value_to_name:
                raise ValueError(f"Duplicate enum value: {i}")
            self._name_to_value[name] = i
            self._value_to_name[i] = name

        # Handle keyword mappings
        for name, value in kwargs.items():
            if not isinstance(name, str):
                raise TypeError(
                    f"Enum name must be a string, got {type(name).__name__}")
            if not isinstance(value, int):
                raise TypeError(
                    f"Enum value must be an integer, got {type(value).__name__}")
            if name in self._name_to_value:
                raise ValueError(f"Duplicate enum name: {name}")
            if value in self._value_to_name:
                raise ValueError(f"Duplicate enum value: {value}")
            self._name_to_value[name] = value
            self._value_to_name[value] = name

    def __call__(self, val):
        """
        Map an integer to its string representation.

        Raises:
            TypeError: if the argument is not an integer.
            ValueError: if the integer is not a valid enum value.
        """
        if not isinstance(val, int):
            raise TypeError(
                f"Enum call expects an integer, got {type(val).__name__}")
        try:
            return self._value_to_name[val]
        except KeyError:
            raise ValueError(f"Invalid enum value: {val}") from None

    def __repr__(self):
        items = ", ".join(f"{name}={value}" for name, value in sorted(
            self._name_to_value.items(), key=lambda x: x[1]))
        return f"<Enum {items}>"

    def __len__(self):
        return len(self._name_to_value)

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self._value_to_name
        if isinstance(item, str):
            return item in self._name_to_value
        return False

    def names(self):
        """Return a list of enum names sorted by their integer values."""
        return [self._value_to_name[i] for i in sorted(self._value_to_name)]

    def values(self):
        """Return a list of enum integer values sorted."""
        return sorted(self._value_to_name)

    def items(self):
        """Return a list of (name, value) tuples sorted by value."""
        return [(self._value_to_name[i], i) for i in sorted(self._value_to_name)]
