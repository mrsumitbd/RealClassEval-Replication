
class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        self.coefficients = None
        self.degree = None

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        self.coefficients = problem.get('coefficients', [])
        self.degree = len(self.coefficients) - 1

        # For simplicity, we'll use numpy's roots function to find the roots
        # Note: This is a basic implementation and may not handle all edge cases
        import numpy as np
        roots = np.roots(self.coefficients)

        # Convert complex roots to real and imaginary parts
        solution = []
        for root in roots:
            if np.iscomplex(root):
                solution.append({'real': root.real, 'imaginary': root.imag})
            else:
                solution.append({'real': root, 'imaginary': 0.0})

        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(solution, list):
            return False

        # Check if the number of roots matches the degree of the polynomial
        expected_roots = len(problem.get('coefficients', [])) - 1
        if len(solution) != expected_roots:
            return False

        # Verify each root satisfies the polynomial equation
        for root in solution:
            if not isinstance(root, dict):
                return False
            real = root.get('real', 0.0)
            imag = root.get('imaginary', 0.0)
            root_value = complex(real, imag)

            # Evaluate the polynomial at the root
            value = 0.0
            for i, coeff in enumerate(problem.get('coefficients', [])):
                value += coeff * \
                    (root_value ** (len(problem.get('coefficients', [])) - 1 - i))

            # Check if the value is close to zero (within a small tolerance)
            if abs(value) > 1e-6:
                return False

        return True
