
class Solver:
    '''Abstract base class for solvers.'''

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return one solution for the given problem.'''
        for solution in self.getSolutionIter(domains, constraints, vconstraints):
            return solution
        return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return all solutions for the given problem.'''
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return an iterator for the solutions of the given problem.'''
        variables = list(domains.keys())

        def is_consistent(assignment, var, value):
            # Check all constraints involving var
            for (constraint, vars_in_constraint) in vconstraints.get(var, []):
                # Only check if all variables in constraint are assigned
                if all(v in assignment or v == var for v in vars_in_constraint):
                    vals = []
                    for v in vars_in_constraint:
                        if v == var:
                            vals.append(value)
                        else:
                            vals.append(assignment[v])
                    if not constraint(*vals):
                        return False
            return True

        def backtrack(assignment):
            if len(assignment) == len(variables):
                yield dict(assignment)
                return
            # Select next unassigned variable
            unassigned = [v for v in variables if v not in assignment]
            if not unassigned:
                return
            var = unassigned[0]
            for value in domains[var]:
                if is_consistent(assignment, var, value):
                    assignment[var] = value
                    yield from backtrack(assignment)
                    del assignment[var]

        yield from backtrack({})
