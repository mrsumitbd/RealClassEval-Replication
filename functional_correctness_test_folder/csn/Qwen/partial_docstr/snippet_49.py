
class QuilAtom:

    def __init__(self, value: str):
        self.value = value

    def out(self) -> str:
        '''Return the element as a valid Quil string.'''
        return self.value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, QuilAtom):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)
