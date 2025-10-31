
class QuilAtom:

    def out(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return True

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)
