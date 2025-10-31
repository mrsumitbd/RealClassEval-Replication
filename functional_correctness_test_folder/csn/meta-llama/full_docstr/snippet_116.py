
from typing import Dict, List, Tuple, Iterator


class Solver:
    '''Abstract base class for solvers.'''

    def getSolution(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> Dict:
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

    def getSolutions(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> List[Dict]:
        '''Return all solutions for the given problem.
        Args:
            domains (dict): Dictionary mapping variables to domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        '''
        return list(self.getSolutionIter(domains, constraints, vconstraints))

    def getSolutionIter(self, domains: Dict, constraints: List[Tuple], vconstraints: Dict) -> Iterator[Dict]:
        '''Return an iterator for the solutions of the given problem.
        Args:
            domains (dict): Dictionary mapping variables to domains
            constraints (list): List of pairs of (constraint, variables)
            vconstraints (dict): Dictionary mapping variables to a list
                of constraints affecting the given variables.
        '''
        raise NotImplementedError("Subclass must implement getSolutionIter")
