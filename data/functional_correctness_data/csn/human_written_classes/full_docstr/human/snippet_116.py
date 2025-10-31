class Solver:
    """Abstract base class for solvers."""
    requires_pickling = False

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return one solution for the given problem.

        Args:
            domains (dict): Dictionary mapping variables to their domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        """
        msg = f'{self.__class__.__name__} is an abstract class'
        raise NotImplementedError(msg)

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return all solutions for the given problem.

        Args:
            domains (dict): Dictionary mapping variables to domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        """
        msg = f'{self.__class__.__name__} provides only a single solution'
        raise NotImplementedError(msg)

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return an iterator for the solutions of the given problem.

        Args:
            domains (dict): Dictionary mapping variables to domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        """
        msg = f"{self.__class__.__name__} doesn't provide iteration"
        raise NotImplementedError(msg)