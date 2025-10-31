
class AccessEnumMixin:
    @classmethod
    def validate(cls, level):
        """
        Validate that `level` is a member of the enum class `cls`.

        Parameters
        ----------
        level : str | cls
            The value to validate. It can be an enum member or a string
            representing the member name.

        Returns
        -------
        cls
            The validated enum member.

        Raises
        ------
        ValueError
            If `level` is a string that does not correspond to a member.
        TypeError
            If `level` is neither a string nor an instance of `cls`.
        """
        if isinstance(level, cls):
            return level

        if isinstance(level, str):
            try:
                return cls[level]
            except KeyError as exc:
                raise ValueError(
                    f"Invalid {cls.__name__} value: {level!r}"
                ) from exc

        raise TypeError(
            f"{cls.__name__}.validate expects a {cls.__name__} or str, "
            f"got {type(level).__name__}"
        )

    def __str__(self):
        """
        Return the name of the enum member.
        """
        return self.name
