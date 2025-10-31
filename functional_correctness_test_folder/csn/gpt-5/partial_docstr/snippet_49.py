class QuilAtom:

    def out(self) -> str:
        '''Return the element as a valid Quil string.'''
        raise NotImplementedError("Subclasses must implement out()")

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilAtom):
            return NotImplemented
        return type(self) is type(other) and self.out() == other.out()

    def __hash__(self) -> int:
        return hash((type(self), self.out()))
