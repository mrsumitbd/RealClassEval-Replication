from typing import IO, List


class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: List[str]):
        '''Initialize enum definition with a name and possible values.'''
        if not isinstance(name, str) or not name:
            raise ValueError("Enum name must be a non-empty string.")
        if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
            raise ValueError(
                "Enum values must be a list of non-empty strings.")
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        target.write(f"{ind}enum class {self.name} {{\n")
        for i, v in enumerate(self.values):
            sep = "," if i < len(self.values) - 1 else ""
            target.write(f"{ind}    {v}{sep}\n")
        target.write(f"{ind}}};\n")
