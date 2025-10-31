
class QuilAtom:

    def out(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"QuilAtom()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, QuilAtom)

    def __hash__(self) -> int:
        return hash("QuilAtom")
