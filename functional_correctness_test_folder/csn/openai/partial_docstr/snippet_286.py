
class AccessEnumMixin:
    @classmethod
    def validate(cls, level):
        """
        Validate and return an enum member from the given *level*.

        Parameters
        ----------
        level : enum member, value, or member name
            The value to validate. It can be an instance of the enum,
            the underlying value of a member, or the member name.

        Returns
        -------
        enum member
            The corresponding enum member.

        Raises
        ------
        ValueError
            If *level* does not correspond to any member of the enum.
        """
        # If already an enum member of the correct type, return it
        if isinstance(level, cls):
            return level

        # Try to interpret *level* as a member value
        if level in cls._value2member_map_:
            return cls._value2member_map_[level]

        # Try to interpret *level* as a member name
        if isinstance(level, str) and level in cls._member_map_:
            return cls._member_map_[level]

        # If none of the above, raise an error
        raise ValueError(f"'{level}' is not a valid {cls.__name__}")

    def __str__(self):
        """Return the string representation of the enum's value."""
        return str(self.value)
