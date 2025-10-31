
from typing import IO, Any


class FieldDefinition:
    '''Prototype of a single field from a class definition.'''

    def __init__(self, name: str, typeStr: str, optional: bool,
                 mapSubject: str, mapPredicate: str, typeDSL: bool):
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
        # Determine the base type
        if self.mapSubject and self.mapPredicate:
            base_type = f"std::map<{self.mapSubject}, {self.mapPredicate}>"
        else:
            base_type = self.typeStr

        # Apply namespace if this is a DSL type
        if self.typeDSL:
            base_type = f"{namespace}::{base_type}"

        # Wrap in std::optional if the field is optional
        if self.optional:
            base_type = f"std::optional<{base_type}>"

        # Write the field definition
        target.write(f"{fullInd}{ind}{base_type} {self.name};\n")
