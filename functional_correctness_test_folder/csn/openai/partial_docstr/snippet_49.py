class QuilAtom:
    def __init__(self, element: str):
        self.element = element

    def out(self) -> str:
        '''Return the element as a valid Quil string.'''
        return self.element

    def __str__(self) -> str:
        return self.element

    def __eq__(self, other: object) -> bool:
        if isinstance(other, QuilAtom):
            return self.element == other.element
        return False

    def __hash__(self) -> int:
        return hash(self.element)
