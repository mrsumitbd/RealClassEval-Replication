
class Solver:
    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return the first solution found or None."""
        gen = self.getSolutionIter(domains, constraints, vconstraints)
        try:
            return next(gen)
        except StopIteration:
            return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return a list of all solutions."""
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Yield all solutions one by one."""
        # Prepare list of variables in a deterministic order
        variables = list(domains.keys())

        # Helper to check all constraints given current assignment
        def constraints_satisfied(assignment):
            # Unary variable constraints
            for var, val in assignment.items():
                if var in vconstraints and not vconstraints[var](val):
                    return False
            # General constraints
            for constraint in constraints:
                # If constraint is a function, call it
                if callable(constraint):
                    try:
                        if not constraint(assignment):
                            return False
                    except Exception:
                        return False
                # If constraint is a tuple of variable names, check consistency
                elif isinstance(constraint, tuple):
                    # Only check if all vars in constraint are assigned
                    if all(v in assignment for v in constraint):
                        values = tuple(assignment[v] for v in constraint)
                        # If values are not all equal, fail
                        if len(set(values)) > 1:
                            return False
                else:
                    # Unsupported constraint type
                    return False
            return True

        def backtrack(assignment, idx):
            if idx == len(variables):
                # All variables assigned
                yield dict(assignment)
                return
            var = variables[idx]
            for val in domains.get(var, []):
                assignment[var] = val
                if constraints_satisfied(assignment):
                    yield from backtrack(assignment, idx + 1)
                # Backtrack
                del assignment[var]

        yield from backtrack({}, 0)
