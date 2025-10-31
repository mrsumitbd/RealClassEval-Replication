
class PolynomialReal:

    def __init__(self):
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
        return self._find_roots()

    def is_solution(self, problem, solution):
        coefficients = problem.get('coefficients', [])
        for root in solution:
            if not self._is_close_to_zero(self._evaluate_polynomial(coefficients, root)):
                return False
        return True

    def _find_roots(self):
        import numpy as np
        return np.roots(self.coefficients).tolist()

    def _evaluate_polynomial(self, coefficients, x):
        return sum(coef * (x ** power) for power, coef in enumerate(reversed(coefficients)))

    def _is_close_to_zero(self, value, tolerance=1e-5):
        return abs(value) < tolerance
