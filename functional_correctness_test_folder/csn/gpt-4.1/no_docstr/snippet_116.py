
class Solver:
    def _is_consistent(self, assignment, constraints, vconstraints):
        # Check binary constraints
        for (var1, var2, func) in constraints:
            if var1 in assignment and var2 in assignment:
                if not func(assignment[var1], assignment[var2]):
                    return False
        # Check variable constraints
        for var, funcs in vconstraints.items():
            if var in assignment:
                for func in funcs:
                    if not func(assignment[var]):
                        return False
        return True

    def _backtrack(self, assignment, domains, constraints, vconstraints):
        if len(assignment) == len(domains):
            return assignment.copy()
        # Select unassigned variable
        unassigned = [v for v in domains if v not in assignment]
        var = unassigned[0]
        for value in domains[var]:
            assignment[var] = value
            if self._is_consistent(assignment, constraints, vconstraints):
                result = self._backtrack(
                    assignment, domains, constraints, vconstraints)
                if result is not None:
                    return result
            del assignment[var]
        return None

    def _backtrack_all(self, assignment, domains, constraints, vconstraints):
        if len(assignment) == len(domains):
            yield assignment.copy()
            return
        unassigned = [v for v in domains if v not in assignment]
        var = unassigned[0]
        for value in domains[var]:
            assignment[var] = value
            if self._is_consistent(assignment, constraints, vconstraints):
                yield from self._backtrack_all(assignment, domains, constraints, vconstraints)
            del assignment[var]

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        return self._backtrack({}, domains, constraints, vconstraints)

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        return list(self._backtrack_all({}, domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        return self._backtrack_all({}, domains, constraints, vconstraints)
