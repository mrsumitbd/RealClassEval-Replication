
from typing import IO


class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: list[str]):
        '''Initialize enum definition with a name and possible values.'''
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        # Open namespace block
        target.write(f"{ind}namespace {common_namespace} {{\n")
        # Write enum declaration
        target.write(f"{ind}    enum {self.name} {{\n")
        # Write enum values
        for i, val in enumerate(self.values):
            comma = ',' if i < len(self.values) - 1 else ''
            target.write(f"{ind}        {val}{comma}\n")
        # Close enum and namespace
        target.write(f"{ind}    }};\n")
        target.write(f"{ind}}}\n")
