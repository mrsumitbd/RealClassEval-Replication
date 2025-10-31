
from typing import IO


class EnumDefinition:

    def __init__(self, name: str, values: list[str]):
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        target.write(f'{ind}enum class {self.name} : int\n')
        target.write(f'{ind}{{\n')
        for i, value in enumerate(self.values):
            target.write(f'{ind}    {value} = {i},\n')
        target.write(f'{ind}}};\n')
