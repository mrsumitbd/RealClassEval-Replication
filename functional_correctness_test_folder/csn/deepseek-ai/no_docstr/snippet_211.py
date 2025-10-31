
from typing import IO, Any


class FieldDefinition:

    def __init__(self, name: str, typeStr: str, optional: bool, mapSubject: str, mapPredicate: str, typeDSL: bool):
        self.name = name
        self.typeStr = typeStr
        self.optional = optional
        self.mapSubject = mapSubject
        self.mapPredicate = mapPredicate
        self.typeDSL = typeDSL

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, namespace: str) -> None:
        target.write(f"{fullInd}{self.name}: ")
        if self.optional:
            target.write("Optional[")
        if self.mapSubject:
            target.write(f"Mapping[{self.mapSubject}, {self.mapPredicate}]")
        else:
            target.write(self.typeStr)
        if self.optional:
            target.write("]")
        if self.typeDSL:
            target.write(
                " = field(default=None)" if self.optional else " = field()")
        target.write("\n")
