
from typing import IO


class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: list[str]):
        '''Initialize enum definition with a name and possible values.'''
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        if common_namespace:
            target.write(f"{ind}class {self.name}(Enum):\n")
        else:
            target.write(f"{ind}from enum import Enum\n")
            target.write(f"{ind}class {self.name}(Enum):\n")
        if not self.values:
            target.write(f"{ind}    pass\n")
        else:
            for v in self.values:
                target.write(f"{ind}    {v} = '{v}'\n")
