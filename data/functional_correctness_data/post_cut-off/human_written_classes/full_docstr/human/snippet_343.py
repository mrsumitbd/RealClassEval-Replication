class Minimize:
    """Class representing a state variable to be minimized in the optimization problem.

    A minimized state variable is one that is optimized to achieve the lowest
    possible value within its bounds.

    Attributes:
        guess: The initial guess value for optimization.
    """

    def __init__(self, guess):
        """Initialize a new minimized state variable.

        Args:
            guess: The initial guess value for optimization.
        """
        self.guess = guess

    def __repr__(self):
        """Get a string representation of this minimized state variable.

        Returns:
            str: A string representation showing the guess value.
        """
        return f'Minimize({self.guess})'