
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
        opt_str = "Optional[" + self.typeStr + \
            "]" if self.optional else self.typeStr
        if self.typeDSL:
            type_repr = f"{namespace}.{self.typeStr}" if namespace else self.typeStr
        else:
            type_repr = opt_str
        map_info = ""
        if self.mapSubject or self.mapPredicate:
            map_info = f"  # mapSubject: {self.mapSubject}, mapPredicate: {self.mapPredicate}"
        line = f"{fullInd}{self.name}: {type_repr}{map_info}\n"
        target.write(line)
