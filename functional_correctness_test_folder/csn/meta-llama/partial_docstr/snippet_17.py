
class Variable:
    '''The representation of a variable with value and type.'''

    def __init__(self, val, _type):
        '''
        :param val:
        :param _type:
        '''
        self.val = val
        self.type = _type

    def __str__(self):
        return f'{self.val} ({self.type})'
