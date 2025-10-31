
class Fix:
    '''Class representing a fixed state variable in the optimization problem.
    A fixed state variable is one that is constrained to a specific value
    and cannot be optimized.
    Attributes:
        value: The fixed value that the state variable must take.
    '''

    def __init__(self, value):
        '''Initialize a new fixed state variable.
        Args:
            value: The fixed value that the state variable must take.
        '''
        self.value = value

    def __repr__(self):
        '''Get a string representation of this fixed state variable.
        Returns:
            str: A string representation showing the fixed value.
        '''
        return f"Fix({self.value})"
