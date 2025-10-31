
class Variable:
    def __init__(self, val, _type):
        """
        Initialize a Variable instance.

        Parameters
        ----------
        val : any
            The value of the variable.
        _type : type or str
            The type of the variable. It can be a Python type object or a string
            representation of the type.
        """
        self.val = val
        self.type = _type

    def __str__(self):
        """
        Return a string representation of the variable's value.

        Returns
        -------
        str
            The string representation of `self.val`.
        """
        return str(self.val)
