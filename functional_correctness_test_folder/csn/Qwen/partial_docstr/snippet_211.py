
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

    def writeDefinition(self, target: 'IO[Any]', fullInd: str, ind: str, namespace: str) -> None:
        '''Write a C++ definition for the class field.'''
        optional_str = '?' if self.optional else ''
        map_info = f', "{self.mapSubject}", "{self.mapPredicate}"' if self.mapSubject and self.mapPredicate else ''
        type_dsl_str = 'true' if self.typeDSL else 'false'
        target.write(
            f'{fullInd}{namespace}Field<{self.typeStr}{optional_str}>{map_info}, {type_dsl_str}> {self.name};\n')
