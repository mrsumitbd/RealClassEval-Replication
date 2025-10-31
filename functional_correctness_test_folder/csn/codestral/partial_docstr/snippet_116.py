
class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return one solution for the given problem.
        Args:
            domains (dict): Dictionary mapping variables to their domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        '''
        from itertools import product

        variables = list(domains.keys())
        assignments = {}

        def backtrack(assignment):
            if len(assignment) == len(variables):
                return assignment

            var = variables[len(assignment)]
            for value in domains[var]:
                new_assignment = assignment.copy()
                new_assignment[var] = value

                if all(constraint(new_assignment) for constraint, vars in constraints if set(vars).issubset(new_assignment)):
                    result = backtrack(new_assignment)
                    if result is not None:
                        return result
            return None

        return backtrack(assignments)

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from itertools import product

        variables = list(domains.keys())
        solutions = []

        def backtrack(assignment):
            if len(assignment) == len(variables):
                solutions.append(assignment.copy())
                return

            var = variables[len(assignment)]
            for value in domains[var]:
                new_assignment = assignment.copy()
                new_assignment[var] = value

                if all(constraint(new_assignment) for constraint, vars in constraints if set(vars).issubset(new_assignment)):
                    backtrack(new_assignment)

        backtrack({})
        return solutions

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from itertools import product

        variables = list(domains.keys())
        assignments = {}

        def backtrack(assignment):
            if len(assignment) == len(variables):
                yield assignment

            var = variables[len(assignment)]
            for value in domains[var]:
                new_assignment = assignment.copy()
                new_assignment[var] = value

                if all(constraint(new_assignment) for constraint, vars in constraints if set(vars).issubset(new_assignment)):
                    yield from backtrack(new_assignment)

        yield from backtrack(assignments)
