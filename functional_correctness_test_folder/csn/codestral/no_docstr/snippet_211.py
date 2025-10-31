
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
        if self.typeDSL:
            target.write(f"{namespace}.{self.typeStr}")
        else:
            target.write(self.typeStr)
        if self.optional:
            target.write("]")
        target.write(
            f" = Field(\n{ind}    default=None,\n{ind}    description=\"\",\n{ind}    title=\"{self.name}\"\n{fullInd})")
