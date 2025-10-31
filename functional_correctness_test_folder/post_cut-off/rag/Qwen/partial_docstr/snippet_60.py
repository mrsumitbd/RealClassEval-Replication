
class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        coefficients = problem.get('coefficients', [])
        target = problem.get('target', 0)
        return self._find_root(coefficients, target)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        coefficients = problem.get('coefficients', [])
        target = problem.get('target', 0)
        return abs(self._evaluate_polynomial(coefficients, solution) - target) < 1e-6

    def _evaluate_polynomial(self, coefficients, x):
        '''Evaluate the polynomial at a given point x.'''
        return sum(coef * (x ** i) for i, coef in enumerate(coefficients))

    def _find_root(self, coefficients, target):
        '''Find a root of the polynomial equation using a simple bisection method.'''
        low, high = -1000, 1000  # Arbitrary large range
        while high - low > 1e-6:
            mid = (low + high) / 2
            if self._evaluate_polynomial(coefficients, mid) < target:
                low = mid
            else:
                high = mid
        return (low + high) / 2
