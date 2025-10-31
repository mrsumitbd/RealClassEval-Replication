class RepeatValueIndicator:
    """Represent a repeating value."""

    def __init__(self, key: str) -> None:
        """Init with key."""
        self.key = key

    def __repr__(self) -> str:
        """Return representation."""
        return f'<same as prior {self.key!r}>'
    __str__ = __repr__