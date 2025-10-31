
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
        # Compose the type string, possibly with namespace
        type_repr = self.typeStr
        if self.typeDSL and namespace:
            type_repr = f"{namespace}::{self.typeStr}"

        # Handle optional
        if self.optional:
            type_repr = f"std::optional<{type_repr}>"

        # Handle mapSubject/mapPredicate (if both are set, it's a map)
        if self.mapSubject and self.mapPredicate:
            # Assume typeStr is the value type
            key_type = "std::string"  # Default to string for key
            value_type = type_repr
            type_repr = f"std::map<{key_type}, {value_type}>"

        # Write the field definition
        target.write(f"{fullInd}{type_repr} {self.name};\n")
