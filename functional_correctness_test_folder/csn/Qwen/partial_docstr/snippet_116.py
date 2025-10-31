
class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return one solution for the given problem.
        Args:
            domains (dict): Dictionary mapping variables to their domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        '''
        def backtrack(assignment):
            if len(assignment) == len(domains):
                return assignment
            var = next(v for v in domains if v not in assignment)
            for value in domains[var]:
                if self.isConsistent(var, value, assignment, constraints):
                    assignment[var] = value
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    del assignment[var]
            return None

        return backtrack({})

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        solutions = []

        def backtrack(assignment):
            if len(assignment) == len(domains):
                solutions.append(assignment.copy())
                return
            var = next(v for v in domains if v not in assignment)
            for value in domains[var]:
                if self.isConsistent(var, value, assignment, constraints):
                    assignment[var] = value
                    backtrack(assignment)
                    del assignment[var]

        backtrack({})
        return solutions

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        def backtrack(assignment):
            if len(assignment) == len(domains):
                yield assignment.copy()
            var = next(v for v in domains if v not in assignment)
            for value in domains[var]:
                if self.isConsistent(var, value, assignment, constraints):
                    assignment[var] = value
                    yield from backtrack(assignment)
                    del assignment[var]

        return backtrack({})

    def isConsistent(self, var, value, assignment, constraints):
        for constraint, variables in constraints:
            if var in variables:
                if not constraint([assignment[v] for v in variables if v in assignment]):
                    return False
        return True
