
class Variable:
    '''The representation of a variable with value and type.'''

    def __init__(self, val, _type):
        '''
        :param val:
        :param _type:
        '''
        self.val = val
        self._type = _type

    def __str__(self):
        return f"Variable(val={self.val}, type={self._type})"
