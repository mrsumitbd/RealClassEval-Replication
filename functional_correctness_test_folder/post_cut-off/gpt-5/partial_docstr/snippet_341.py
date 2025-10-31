class Free:

    def __init__(self, guess):
        '''Initialize a new free state variable.
        Args:
            guess: The initial guess value for optimization.
        '''
        self.guess = guess
        self.value = guess

    def __repr__(self):
        return f"Free(guess={self.guess!r})"
