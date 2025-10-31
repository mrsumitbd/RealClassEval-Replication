
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
        # Expecting problem to have a key 'coefficients' which is a list of real numbers
        # representing the polynomial coefficients in decreasing order of degree.
        # Return all real roots as a sorted list.
        import numpy as np

        coeffs = problem.get('coefficients', [])
        if not coeffs or not isinstance(coeffs, list):
            return []

        # Remove leading zeros
        while coeffs and coeffs[0] == 0:
            coeffs = coeffs[1:]
        if not coeffs:
            return []

        roots = np.roots(coeffs)
        # Filter real roots (imaginary part close to zero)
        real_roots = [float(r.real) for r in roots if abs(r.imag) < 1e-8]
        # Remove duplicates due to numerical errors
        real_roots = list(set([round(r, 8) for r in real_roots]))
        real_roots.sort()
        return real_roots

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        coeffs = problem.get('coefficients', [])
        if not coeffs or not isinstance(coeffs, list):
            return solution == []

        # Remove leading zeros
        while coeffs and coeffs[0] == 0:
            coeffs = coeffs[1:]
        if not coeffs:
            return solution == []

        # Check that each value in solution is a real root
        for x in solution:
            # Evaluate polynomial at x
            val = 0
            for i, c in enumerate(coeffs):
                val += c * (x ** (len(coeffs) - i - 1))
            if abs(val) > 1e-6:
                return False

        # Check that all real roots are included (within tolerance)
        import numpy as np
        roots = np.roots(coeffs)
        real_roots = [float(r.real) for r in roots if abs(r.imag) < 1e-8]
        real_roots = list(set([round(r, 8) for r in real_roots]))
        real_roots.sort()
        # Compare sorted lists
        sol_sorted = sorted([round(x, 8) for x in solution])
        return sol_sorted == real_roots
