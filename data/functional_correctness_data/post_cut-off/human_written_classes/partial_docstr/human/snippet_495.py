from dataclasses import dataclass

@dataclass
class NamedValue:
    """
    Represents a named value within API Management.
    """
    name: str
    value: str
    isSecret: bool = False

    def __init__(self, name: str, value: str, isSecret: bool=False) -> None:
        self.name = name
        self.value = value
        self.isSecret = isSecret

    def to_dict(self) -> dict:
        nv_dict = {'name': self.name, 'value': self.value, 'isSecret': self.isSecret}
        return nv_dict