class QuilAtom:
    """Abstract class for atomic elements of Quil."""

    def out(self) -> str:
        """Return the element as a valid Quil string."""
        raise NotImplementedError()

    def __str__(self) -> str:
        """Get a string representation of the element, possibly not valid Quil."""
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        """Return True if the other object is equal to this one."""
        raise NotImplementedError()

    def __hash__(self) -> int:
        """Return a hash of the object."""
        raise NotImplementedError()