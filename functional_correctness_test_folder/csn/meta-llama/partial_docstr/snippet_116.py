
from typing import Dict, List, Tuple, Iterator


class Solver:

    def getSolution(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict):
        '''Return one solution for the given problem.
        Args:
            domains (dict): Dictionary mapping variables to their domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        '''
        solution_iter = self.getSolutionIter(
            domains, constraints, vconstraints)
        try:
            return next(solution_iter)
        except StopIteration:
            return None

    def getSolutions(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict):
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> Iterator[Dict]:
        variables = list(domains.keys())
        assignment = {var: None for var in variables}

        def is_consistent(assignment, var, value):
            for constraint, vars_involved in constraints:
                if var in vars_involved:
                    vars_to_check = [
                        v for v in vars_involved if v in assignment]
                    if not constraint({v: assignment[v] for v in vars_to_check}):
                        return False
            return True

        def backtrack(assignment, index=0):
            if index == len(variables):
                yield assignment.copy()
            else:
                var = variables[index]
                for value in domains[var]:
                    if is_consistent(assignment, var, value):
                        assignment[var] = value
                        yield from backtrack(assignment, index + 1)
                        assignment[var] = None

        yield from backtrack(assignment)
