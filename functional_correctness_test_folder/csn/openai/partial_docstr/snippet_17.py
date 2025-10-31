
class Variable:
    '''The representation of a variable with value and type.'''

    def __init__(self, val, _type):
        """
        :param val: The value of the variable.
        :param _type: The type of the variable. Can be a type object or a string.
        """
        self.val = val
        # Normalise the type representation
        if isinstance(_type, type):
            self._type = _type.__name__
        else:
            self._type = str(_type)

    def __str__(self):
        return f"{self.val} ({self._type})"
