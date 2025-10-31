
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
        # Resolve the type string, adding namespace if needed
        if self.typeDSL:
            # If the type is a DSL type, prepend the namespace
            type_name = f"{namespace}::{self.typeStr}" if namespace else self.typeStr
        else:
            type_name = self.typeStr

        # Wrap in std::optional if the field is optional
        if self.optional:
            type_decl = f"std::optional<{type_name}>"
        else:
            type_decl = type_name

        # Write the field declaration
        target.write(f"{fullInd}{type_decl} {self.name};\n")
