from collections.abc import Sequence
from constraint.domain import Unassigned

class Constraint:
    """Abstract base class for constraints."""

    def __call__(self, variables: Sequence, domains: dict, assignments: dict, forwardcheck=False):
        """Perform the constraint checking.

        If the forwardcheck parameter is not false, besides telling if
        the constraint is currently broken or not, the constraint
        implementation may choose to hide values from the domains of
        unassigned variables to prevent them from being used, and thus
        prune the search space.

        Args:
            variables (sequence): :py:class:`Variables` affected by that constraint,
                in the same order provided by the user
            domains (dict): Dictionary mapping variables to their
                domains
            assignments (dict): Dictionary mapping assigned variables to
                their current assumed value
            forwardcheck: Boolean value stating whether forward checking
                should be performed or not

        Returns:
            bool: Boolean value stating if this constraint is currently
            broken or not
        """
        return True

    def preProcess(self, variables: Sequence, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Preprocess variable domains.

        This method is called before starting to look for solutions,
        and is used to prune domains with specific constraint logic
        when possible. For instance, any constraints with a single
        variable may be applied on all possible values and removed,
        since they may act on individual values even without further
        knowledge about other assignments.

        Args:
            variables (sequence): Variables affected by that constraint,
                in the same order provided by the user
            domains (dict): Dictionary mapping variables to their
                domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        """
        if len(variables) == 1:
            variable = variables[0]
            domain = domains[variable]
            for value in domain[:]:
                if not self(variables, domains, {variable: value}):
                    domain.remove(value)
            constraints.remove((self, variables))
            vconstraints[variable].remove((self, variables))

    def forwardCheck(self, variables: Sequence, domains: dict, assignments: dict, _unassigned=Unassigned):
        """Helper method for generic forward checking.

        Currently, this method acts only when there's a single
        unassigned variable.

        Args:
            variables (sequence): Variables affected by that constraint,
                in the same order provided by the user
            domains (dict): Dictionary mapping variables to their
                domains
            assignments (dict): Dictionary mapping assigned variables to
                their current assumed value

        Returns:
            bool: Boolean value stating if this constraint is currently
            broken or not
        """
        unassignedvariable = _unassigned
        for variable in variables:
            if variable not in assignments:
                if unassignedvariable is _unassigned:
                    unassignedvariable = variable
                else:
                    break
        else:
            if unassignedvariable is not _unassigned:
                domain = domains[unassignedvariable]
                if domain:
                    for value in domain[:]:
                        assignments[unassignedvariable] = value
                        if not self(variables, domains, assignments):
                            domain.hideValue(value)
                    del assignments[unassignedvariable]
                if not domain:
                    return False
        return True