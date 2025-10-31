
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = np.array(problem['A'], dtype=complex)
        _, v = np.linalg.eig(A)
        # Return as list of lists of complex numbers
        return v.tolist()

    def is_solution(self, problem, solution):
        A = np.array(problem['A'], dtype=complex)
        v = np.array(solution, dtype=complex)
        # v should be (n, n) where each column is an eigenvector
        # Check for each eigenvector if Av = lambda v for some lambda
        n = v.shape[1]
        for i in range(n):
            vec = v[:, i]
            if np.allclose(vec, 0):
                return False
            Av = A @ vec
            # Find scalar lambda: Av = lambda * v
            # If v[j] != 0, lambda = Av[j]/v[j]
            nonzero = np.where(np.abs(vec) > 1e-8)[0]
            if len(nonzero) == 0:
                return False
            lambdas = Av[nonzero] / vec[nonzero]
            # All lambdas should be (almost) equal
            if not np.allclose(lambdas, lambdas[0], atol=1e-6):
                return False
            # Also check Av ≈ lambda * v
            if not np.allclose(Av, lambdas[0] * vec, atol=1e-6):
                return False
        return True
