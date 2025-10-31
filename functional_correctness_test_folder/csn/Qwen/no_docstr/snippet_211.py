
class FieldDefinition:

    def __init__(self, name: str, typeStr: str, optional: bool, mapSubject: str, mapPredicate: str, typeDSL: bool):
        self.name = name
        self.typeStr = typeStr
        self.optional = optional
        self.mapSubject = mapSubject
        self.mapPredicate = mapPredicate
        self.typeDSL = typeDSL

    def writeDefinition(self, target: 'IO[Any]', fullInd: str, ind: str, namespace: str) -> None:
        optional_str = "?" if self.optional else ""
        type_dsl_str = " (typeDSL)" if self.typeDSL else ""
        definition = f"{fullInd}{self.name}{optional_str}: {namespace}{self.typeStr}{type_dsl_str}  # {self.mapSubject} {self.mapPredicate}\n"
        target.write(definition)
