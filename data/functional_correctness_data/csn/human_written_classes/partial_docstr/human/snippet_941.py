class Color:
    """Represent an ANSI escape sequence"""

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f'Color({self.name})'