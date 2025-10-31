class Variable:
    '''Helper class for variable definition.
    Using this class is optional, since any hashable object,
    including plain strings and integers, may be used as variables.
    '''

    def __init__(self, name):
        '''Initialization method.
        Args:
            name (string): Generic variable name for problem-specific
                purposes
        '''
        self.name = name

    def __repr__(self):
        '''Represents itself with the name attribute.'''
        return f'{self.name}'
