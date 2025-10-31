
class QuilAtom:
    def __init__(self, value):
        self.value = value

    def out(self) -> str:
        if isinstance(self.value, str):
            # If the string contains spaces or special chars, quote it
            if not self.value.isidentifier():
                return f'"{self.value}"'
            return self.value
        elif isinstance(self.value, bool):
            return "TRUE" if self.value else "FALSE"
        elif isinstance(self.value, (int, float)):
            return str(self.value)
        else:
            return str(self.value)

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilAtom):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
