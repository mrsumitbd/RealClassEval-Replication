class Enum:
    __slots__ = 'elements'

    def __init__(self, *elements: str) -> None:
        self.elements = tuple(elements)

    def __getattr__(self, name: str) -> str:
        if name not in self.elements:
            raise AttributeError(f"'Enum' has no attribute '{name}'")
        return name