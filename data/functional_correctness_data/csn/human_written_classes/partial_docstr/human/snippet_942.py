class Alias:
    """
    An alias object used to resolve aliases for engine names.
    """

    def __init__(self, target: str) -> None:
        self.target = target

    def __repr__(self) -> str:
        return f'<Alias to "{self.target}">'