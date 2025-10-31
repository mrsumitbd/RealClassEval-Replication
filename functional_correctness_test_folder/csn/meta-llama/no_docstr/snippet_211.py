
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
        target.write(f'{ind}public {self.name}: {self.typeStr}' +
                     (' | null' if self.optional else '') + ';\n')
        if self.mapSubject or self.mapPredicate:
            target.write(
                f'{ind}static get {self.name}(): PropertyMapping {{\n')
            target.write(
                f'{ind}    return new PropertyMapping("{self.mapSubject or fullInd}", "{self.mapPredicate or self.name}")\n')
            target.write(f'{ind}}}\n')
        if self.typeDSL:
            target.write(f'{ind}static get {self.name}Type(): TypeDef {{\n')
            target.write(
                f'{ind}    return new TypeDef("{namespace}.{self.typeStr}")\n')
            target.write(f'{ind}}}\n')
