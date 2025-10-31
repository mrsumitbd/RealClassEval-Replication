
class Variable:
    '''The representation of a variable with value and type.'''

    def __init__(self, val, _type):
        '''
        :param val: The value of the variable.
        :param _type: The type of the variable.
        '''
        self.val = val
        self._type = _type

    def __str__(self):
        '''
        :return: A string representation of the variable.
        '''
        return f"Variable(val={self.val}, type={self._type})"
