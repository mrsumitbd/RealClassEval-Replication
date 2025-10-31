class PropertyXWithInt:
    """Class with a property x and an __int__ method"""

    @property
    def x(self) -> int:
        return 42

    def __int__(self):
        return 42