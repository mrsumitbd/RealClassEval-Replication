
class Solver:
    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return one solution for the given problem.'''
        for solution in self.getSolutionIter(domains, constraints, vconstraints):
            return solution
        return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return all solutions for the given problem.'''
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Yield all solutions for the given problem.'''
        variables = list(domains.keys())

        def is_consistent(var, value, assignment):
            # Check all constraints involving var
            for constraint, cvars in vconstraints.get(var, []):
                # Build the values for the constraint variables
                vals = []
                for v in cvars:
                    if v == var:
                        vals.append(value)
                    elif v in assignment:
                        vals.append(assignment[v])
                    else:
                        break
                else:
                    # All variables assigned, check constraint
                    if not constraint(*vals):
                        return False
            return True

        def backtrack(assignment):
            if len(assignment) == len(variables):
                yield dict(assignment)
                return
            # Select unassigned variable
            unassigned = [v for v in variables if v not in assignment]
            var = unassigned[0]
            for value in domains[var]:
                if is_consistent(var, value, assignment):
                    assignment[var] = value
                    yield from backtrack(assignment)
                    del assignment[var]

        yield from backtrack({})
