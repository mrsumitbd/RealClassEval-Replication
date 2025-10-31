
import itertools


class Solver:

    def getSolution(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        '''Return one solution for the given problem.
        Args:
            domains (dict): Dictionary mapping variables to their domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        '''
        solution = {}
        remaining_vars = list(domains.keys())

        def backtrack():
            if not remaining_vars:
                return solution.copy()

            var = remaining_vars.pop()
            for value in domains[var]:
                solution[var] = value
                consistent = True
                for constraint, affected_vars in vconstraints.get(var, []):
                    if not constraint(solution):
                        consistent = False
                        break
                if consistent:
                    result = backtrack()
                    if result is not None:
                        return result
                del solution[var]
            remaining_vars.append(var)
            return None

        return backtrack()

    def getSolutions(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        solutions = []
        remaining_vars = list(domains.keys())

        def backtrack():
            if not remaining_vars:
                solutions.append({k: v for k, v in solution.items()})
                return

            var = remaining_vars.pop()
            for value in domains[var]:
                solution[var] = value
                consistent = True
                for constraint, affected_vars in vconstraints.get(var, []):
                    if not constraint(solution):
                        consistent = False
                        break
                if consistent:
                    backtrack()
                del solution[var]
            remaining_vars.append(var)

        solution = {}
        backtrack()
        return solutions

    def getSolutionIter(self, domains: dict, constraints: list[tuple], vconstraints: dict):
        remaining_vars = list(domains.keys())
        stack = []
        solution = {}

        def push_stack(var_index):
            if var_index >= len(remaining_vars):
                yield solution.copy()
                return

            var = remaining_vars[var_index]
            for value in domains[var]:
                solution[var] = value
                consistent = True
                for constraint, affected_vars in vconstraints.get(var, []):
                    if not constraint(solution):
                        consistent = False
                        break
                if consistent:
                    for result in push_stack(var_index + 1):
                        yield result
                del solution[var]

        return push_stack(0)
