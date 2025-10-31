
class QuilAtom:
    def __init__(self, value):
        self.value = value

    def out(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilAtom):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
