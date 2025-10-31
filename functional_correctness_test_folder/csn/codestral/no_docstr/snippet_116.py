
class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from itertools import product

        variables = list(domains.keys())
        values = list(product(*domains.values()))

        for value in values:
            assignment = dict(zip(variables, value))
            if all(constraint(assignment) for constraint in constraints):
                if all(vconstraints[var](assignment[var]) for var in vconstraints):
                    return assignment
        return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from itertools import product

        variables = list(domains.keys())
        values = list(product(*domains.values()))
        solutions = []

        for value in values:
            assignment = dict(zip(variables, value))
            if all(constraint(assignment) for constraint in constraints):
                if all(vconstraints[var](assignment[var]) for var in vconstraints):
                    solutions.append(assignment)
        return solutions

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        from itertools import product

        variables = list(domains.keys())
        values = product(*domains.values())

        for value in values:
            assignment = dict(zip(variables, value))
            if all(constraint(assignment) for constraint in constraints):
                if all(vconstraints[var](assignment[var]) for var in vconstraints):
                    yield assignment
