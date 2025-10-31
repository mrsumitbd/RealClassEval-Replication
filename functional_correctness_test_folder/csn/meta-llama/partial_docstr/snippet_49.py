
class QuilAtom:
    def __init__(self, name: str):
        """
        Initialize a QuilAtom instance.

        Args:
        name (str): The name of the QuilAtom.
        """
        self.name = name

    def out(self) -> str:
        '''Return the element as a valid Quil string.'''
        return self.name

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilAtom):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
