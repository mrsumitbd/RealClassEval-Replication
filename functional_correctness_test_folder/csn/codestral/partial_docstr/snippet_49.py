
class QuilAtom:

    def out(self) -> str:
        '''Return the element as a valid Quil string.'''
        return str(self)

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilAtom):
            return False
        return str(self) == str(other)

    def __hash__(self) -> int:
        return hash(str(self))
