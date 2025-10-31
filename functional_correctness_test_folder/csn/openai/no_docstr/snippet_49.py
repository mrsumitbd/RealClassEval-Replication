
class QuilAtom:
    def __init__(self, name: str, value: str | None = None):
        self.name = name
        self.value = value

    def out(self) -> str:
        return f"{self.name} {self.value}" if self.value is not None else self.name

    def __str__(self) -> str:
        return f"QuilAtom(name={self.name!r}, value={self.value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilAtom):
            return False
        return self.name == other.name and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.name, self.value))
