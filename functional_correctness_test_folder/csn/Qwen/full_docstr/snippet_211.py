
class FieldDefinition:
    '''Prototype of a single field from a class definition.'''

    def __init__(self, name: str, typeStr: str, optional: bool, mapSubject: str, mapPredicate: str, typeDSL: bool):
        '''Initialize field definition.
        Creates a new field with name, its type, optional and which field to use to convert
        from list to map (or empty if it is not possible)
        '''
        self.name = name
        self.typeStr = typeStr
        self.optional = optional
        self.mapSubject = mapSubject
        self.mapPredicate = mapPredicate
        self.typeDSL = typeDSL

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, namespace: str) -> None:
        '''Write a C++ definition for the class field.'''
        optional_str = " = nullptr" if self.optional else ""
        if self.typeDSL:
            type_str = f"{namespace}::{self.typeStr}"
        else:
            type_str = self.typeStr

        if self.mapSubject and self.mapPredicate:
            map_info = f" // Maps {self.mapSubject} by {self.mapPredicate}"
        else:
            map_info = ""

        target.write(
            f"{fullInd}{type_str}* {self.name}{optional_str};{map_info}\n")
