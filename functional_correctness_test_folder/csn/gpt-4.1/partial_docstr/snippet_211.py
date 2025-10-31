
from typing import IO, Any


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
        # Compose the C++ type
        cpp_type = self.typeStr
        if self.typeDSL and namespace:
            cpp_type = f"{namespace}::{self.typeStr}"
        if self.mapSubject and self.mapPredicate:
            cpp_type = f"std::map<{self.mapSubject}, {self.mapPredicate}>"
        if self.optional:
            cpp_type = f"std::optional<{cpp_type}>"
        # Write the field definition
        target.write(f"{fullInd}{cpp_type} {self.name};\n")
