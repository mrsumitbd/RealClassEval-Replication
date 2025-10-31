
from typing import Dict, List, Tuple, Iterator


class Solver:

    def getSolution(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> Dict:
        """Get the first solution that satisfies the given constraints."""
        solutions = self.getSolutions(domains, constraints, vconstraints)
        return next(iter(solutions), None)

    def getSolutions(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> List[Dict]:
        """Get all solutions that satisfy the given constraints."""
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> Iterator[Dict]:
        """Get an iterator over all solutions that satisfy the given constraints."""

        # Check if the domains are empty
        if not domains:
            yield {}
            return

        # Get the variables and their domains
        variables = list(domains.keys())

        def is_valid(assignment: Dict) -> bool:
            """Check if the given assignment satisfies the constraints."""
            for constraint in constraints:
                func, vars_involved = constraint
                vars_involved_values = [assignment[var]
                                        for var in vars_involved if var in assignment]
                if len(vars_involved_values) == len(vars_involved) and not func(*vars_involved_values):
                    return False
            for var, func in vconstraints.items():
                if var in assignment and not func(assignment[var]):
                    return False
            return True

        def backtrack(assignment: Dict = {}) -> Iterator[Dict]:
            """Recursively try all possible assignments."""
            if len(assignment) == len(variables):
                if is_valid(assignment):
                    yield assignment
            else:
                var = next((v for v in variables if v not in assignment), None)
                for value in domains[var]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = value
                    yield from backtrack(new_assignment)

        yield from backtrack()
