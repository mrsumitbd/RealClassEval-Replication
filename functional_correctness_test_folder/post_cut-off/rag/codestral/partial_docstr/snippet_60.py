
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
        if not solution:
            return False

        # Reconstruct the polynomial from the roots
        reconstructed_coeffs = [1.0]  # Start with x^0 term
        for root in solution:
            real = root.get('real', 0.0)
            imaginary = root.get('imaginary', 0.0)
            if imaginary != 0.0:
                # Complex conjugate pair
                root1 = complex(real, imaginary)
                root2 = complex(real, -imaginary)
                # Multiply by (x - root1) and (x - root2)
                reconstructed_coeffs = np.convolve(
                    reconstructed_coeffs, [1, -root1])
                reconstructed_coeffs = np.convolve(
                    reconstructed_coeffs, [1, -root2])
            else:
                # Real root
                reconstructed_coeffs = np.convolve(
                    reconstructed_coeffs, [1, -real])

        # Compare with original coefficients (allowing for floating point precision)
        original_coeffs = problem.get('coefficients', [])
        if len(reconstructed_coeffs) != len(original_coeffs):
            return False

        for orig, recon in zip(original_coeffs, reconstructed_coeffs):
            if not np.isclose(orig, recon, rtol=1e-5, atol=1e-8):
                return False

        return True
