class QuilAtom:
    def out(self) -> str:
        raise NotImplementedError(
            "Subclasses must implement 'out' to return a string representation.")

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        return self is other

    def __hash__(self) -> int:
        return id(self)
