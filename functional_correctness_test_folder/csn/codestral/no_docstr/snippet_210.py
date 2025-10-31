
class EnumDefinition:

    def __init__(self, name: str, values: list[str]):

        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:

        target.write(f"{ind}class {self.name}(Enum):\n")
        for value in self.values:
            target.write(f"{ind}    {value} = auto()\n")
