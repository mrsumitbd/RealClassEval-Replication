
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
        if self.typeDSL:
            typeStr = f'{namespace}::{self.typeStr}'
        else:
            typeStr = self.typeStr

        if self.optional:
            declaration = f'std::optional<{typeStr}> {self.name};'
        else:
            declaration = f'{typeStr} {self.name};'

        target.write(f'{fullInd}{declaration}\n')

        if self.mapSubject or self.mapPredicate:
            target.write(
                f'{fullInd}// Conversion from list to map is possible using {self.mapSubject or self.mapPredicate}\n')
