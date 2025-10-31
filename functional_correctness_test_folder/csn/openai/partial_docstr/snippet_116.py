
class Solver:
    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return one solution for the given problem or None if none exists."""
        for solution in self.getSolutionIter(domains, constraints, vconstraints):
            return solution
        return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Return a list of all solutions for the given problem."""
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        """Yield all solutions for the given problem."""
        # Make a shallow copy of domains to avoid side effects
        domains = {var: list(vals) for var, vals in domains.items()}
        # Build a mapping from variable to constraints for quick lookup
        var_to_constraints = vconstraints

        # Helper to check all constraints that are fully assigned
        def constraints_satisfied(assignment):
            for var, cons_list in var_to_constraints.items():
                if var in assignment:
                    for constraint, vars_involved in cons_list:
                        # Only evaluate if all vars involved are assigned
                        if all(v in assignment for v in vars_involved):
                            if not constraint(assignment):
                                return False
            return True

        # Recursive backtracking search
        def backtrack(assignment):
            # If all variables assigned, yield solution
            if len(assignment) == len(domains):
                yield dict(assignment)
                return

            # Select unassigned variable with smallest domain (MRV heuristic)
            unassigned = [v for v in domains if v not in assignment]
            var = min(unassigned, key=lambda v: len(domains[v]))

            for value in domains[var]:
                assignment[var] = value
                if constraints_satisfied(assignment):
                    yield from backtrack(assignment)
                del assignment[var]

        yield from backtrack({})
