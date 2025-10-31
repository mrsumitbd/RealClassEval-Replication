
import numpy as np


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
        coefficients = problem['coefficients']
        lower_bound = problem['lower_bound']
        upper_bound = problem['upper_bound']
        target = problem.get('target', 0.0)
        max_iter = problem.get('max_iter', 1000)
        tol = problem.get('tol', 1e-6)

        def func(x):
            return np.polyval(coefficients, x) - target

        x = np.linspace(lower_bound, upper_bound, 1000)
        y = func(x)

        # Find the roots using a simple iterative method
        roots = []
        for i in range(len(x) - 1):
            if y[i] * y[i + 1] < 0:
                root = (x[i] + x[i + 1]) / 2.0
                for _ in range(max_iter):
                    root_new = root - \
                        func(root) / np.polyval(np.polyder(coefficients), root)
                    if abs(root_new - root) < tol:
                        roots.append(root_new)
                        break
                    root = root_new

        return {'roots': roots}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        coefficients = problem['coefficients']
        target = problem.get('target', 0.0)
        tol = problem.get('tol', 1e-6)
        roots = solution.get('roots', [])

        for root in roots:
            if abs(np.polyval(coefficients, root) - target) > tol:
                return False

        return True
