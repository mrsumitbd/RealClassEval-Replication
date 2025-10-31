
from typing import IO


class EnumDefinition:

    def __init__(self, name: str, values: list[str]):
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        if common_namespace:
            target.write(f"{ind}namespace {common_namespace} {{\n")
            ind += "    "
        target.write(f"{ind}enum {self.name} {{\n")
        for i, value in enumerate(self.values):
            comma = "," if i < len(self.values) - 1 else ""
            target.write(f"{ind}    {value}{comma}\n")
        target.write(f"{ind}}}\n")
        if common_namespace:
            ind = ind[:-4]
            target.write(f"{ind}}}\n")
