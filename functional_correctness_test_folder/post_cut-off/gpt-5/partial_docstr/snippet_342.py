class Maximize:
    '''Class representing a state variable to be maximized in the optimization problem.
    A maximized state variable is one that is optimized to achieve the highest
    possible value within its bounds.
    Attributes:
        guess: The initial guess value for optimization.
    '''

    def __init__(self, guess):
        self.guess = guess

    def __repr__(self):
        '''Get a string representation of this maximized state variable.
        Returns:
            str: A string representation showing the guess value.
        '''
        return f"Maximize(guess={self.guess!r})"
