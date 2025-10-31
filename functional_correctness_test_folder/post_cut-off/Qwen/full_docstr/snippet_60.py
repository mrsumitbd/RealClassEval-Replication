
class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        self.coefficients = []

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        self.coefficients = problem.get('coefficients', [])
        return self.find_roots()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        self.coefficients = problem.get('coefficients', [])
        for root in solution:
            if not self.is_close_to_zero(self.evaluate(root)):
                return False
        return True

    def evaluate(self, x):
        '''Evaluate the polynomial at x.'''
        return sum(coef * (x ** power) for power, coef in enumerate(self.coefficients))

    def find_roots(self):
        '''Find the roots of the polynomial using numpy.'''
        import numpy as np
        return np.roots(self.coefficients[::-1]).tolist()

    def is_close_to_zero(self, value, tolerance=1e-5):
        '''Check if a value is close to zero within a given tolerance.'''
        return abs(value) < tolerance
