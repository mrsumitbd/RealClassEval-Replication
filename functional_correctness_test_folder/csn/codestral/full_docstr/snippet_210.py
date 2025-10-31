
class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: list[str]):
        '''Initialize enum definition with a name and possible values.'''
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        target.write(f"{ind}class {self.name}(Enum):\n")
        for value in self.values:
            target.write(f"{ind}    {value} = auto()\n")
