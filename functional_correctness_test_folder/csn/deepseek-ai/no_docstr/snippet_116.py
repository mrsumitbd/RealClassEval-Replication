
class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        try:
            return next(self.getSolutionIter(domains, constraints, vconstraints))
        except StopIteration:
            return None

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        assignments = {}

        def backtrack(assignments):
            if len(assignments) == len(domains):
                yield assignments.copy()
                return

            var = select_unassigned_variable(domains, assignments)
            for value in domains[var]:
                assignments[var] = value
                if is_consistent(var, assignments, constraints, vconstraints):
                    yield from backtrack(assignments)
                del assignments[var]

        def select_unassigned_variable(domains, assignments):
            unassigned = [var for var in domains if var not in assignments]
            return min(unassigned, key=lambda var: len(domains[var]))

        def is_consistent(var, assignments, constraints, vconstraints):
            for constraint in vconstraints.get(var, []):
                variables, func = constraint
                args = [assignments.get(v, None) for v in variables]
                if None not in args and not func(*args):
                    return False
            return True

        yield from backtrack(assignments)
