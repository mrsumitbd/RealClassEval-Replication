
class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: list[str]):
        '''Initialize enum definition with a name and possible values.'''
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        target.write(f"{ind}class {self.name}:\n")
        target.write(f"{ind}    '''Enum class for {self.name}.'''\n")
        for value in self.values:
            target.write(f"{ind}    {value} = '{value}'\n")
        target.write(f"{ind}\n")
        target.write(f"{ind}    @classmethod\n")
        target.write(f"{ind}    def values(cls) -> list[str]:\n")
        target.write(f"{ind}        '''Return a list of all enum values.'''\n")
        target.write(
            f"{ind}        return [{', '.join(f'cls.{value}' for value in self.values)}]\n")
