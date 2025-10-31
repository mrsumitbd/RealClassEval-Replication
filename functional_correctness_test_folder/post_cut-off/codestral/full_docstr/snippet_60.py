
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
        roots = self._find_roots()
        return {'roots': roots}

    def _find_roots(self):
        '''
        Find the roots of the polynomial using the coefficients.
        Returns:
            List of roots of the polynomial
        '''
        roots = []
        if len(self.coefficients) == 0:
            return roots

        # For simplicity, we'll use a basic method to find roots
        # This can be improved using more advanced methods like Newton-Raphson
        for i in range(1, 1000):
            x = i / 100
            y = self._evaluate_polynomial(x)
            if abs(y) < 0.01:
                roots.append(x)

        return roots

    def _evaluate_polynomial(self, x):
        '''
        Evaluate the polynomial at a given point x.
        Args:
            x: The point at which to evaluate the polynomial
        Returns:
            The value of the polynomial at x
        '''
        result = 0
        for i, coeff in enumerate(self.coefficients):
            result += coeff * (x ** i)
        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if 'roots' not in solution:
            return False

        roots = solution['roots']
        coefficients = problem.get('coefficients', [])

        for root in roots:
            if abs(self._evaluate_polynomial(root)) > 0.01:
                return False

        return True
