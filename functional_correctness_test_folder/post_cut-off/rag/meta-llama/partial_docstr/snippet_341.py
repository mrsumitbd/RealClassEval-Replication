class Free:
    """Class representing a free state variable in the optimization problem.

    A free state variable is one that is not constrained to any specific value
    but can be optimized within its bounds.

    Attributes:
        guess: The initial guess value for optimization.
    """

    def __init__(self, guess):
        """Initialize a new free state variable.

        Args:
            guess: The initial guess value for optimization.
        """
        self.guess = guess

    def __repr__(self):
        """Get a string representation of this free state variable.

        Returns:
            str: A string representation showing the guess value.
        """
        return 'Free(guess={})'.format(self.guess)
