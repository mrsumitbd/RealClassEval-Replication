class Free:

    def __init__(self, guess):
        '''Initialize a new free state variable.
        Args:
            guess: The initial guess value for optimization.
        '''
        self.guess = guess

    def __repr__(self):
        return f"Free({self.guess!r})"
