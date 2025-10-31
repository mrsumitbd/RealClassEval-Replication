import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def _get_matrix(self, problem):
        for key in ('A', 'matrix', 'M', 'data'):
            if key in problem:
                A = np.asarray(problem[key], dtype=complex)
                return A
        return None

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = self._get_matrix(problem)
        if A is None:
            return None
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return None

        # Compute eigen decomposition
        w, V = np.linalg.eig(A)

        # Sort eigenpairs for determinism by (real, imag)
        order = np.lexsort((w.imag, w.real))
        w = w[order]
        V = V[:, order]

        # Normalize eigenvectors and fix phase: make the largest magnitude entry real and non-negative
        for k in range(V.shape[1]):
            vec = V[:, k]
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
                idx = int(np.argmax(np.abs(vec)))
                if np.abs(vec[idx]) > 0:
                    phase = np.exp(-1j * np.angle(vec[idx]))
                    vec = vec * phase
            V[:, k] = vec

        return {
            'eigenvalues': w.tolist(),
            'eigenvectors': V.tolist()
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = self._get_matrix(problem)
        if A is None or A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False

        n = A.shape[0]
        tol = float(problem.get('tol', 1e-6))

        # Extract eigenvectors
        V = None
        for key in ('eigenvectors', 'vectors', 'V'):
            if isinstance(solution, dict) and key in solution:
                V = np.asarray(solution[key], dtype=complex)
                break
        if V is None:
            return False

        # Ensure V shape: either (n, k) with k >= 1, or (k, n) where rows are vectors -> convert
        if V.ndim != 2:
            return False
        if V.shape[0] != n and V.shape[1] != n:
            return False
        if V.shape[0] != n and V.shape[1] == n:
            V = V.T  # transpose to (n, n or k)

        # Extract eigenvalues if provided; otherwise compute via Rayleigh quotient
        lambdas = None
        for key in ('eigenvalues', 'values', 'w', 'lambdas'):
            if isinstance(solution, dict) and key in solution:
                arr = np.asarray(solution[key], dtype=complex).ravel()
                lambdas = arr
                break

        k = V.shape[1]
        if lambdas is not None and lambdas.shape[0] != k:
            # If counts mismatch, ignore provided and compute via Rayleigh
            lambdas = None

        # Precompute matrix norm for relative tolerance
        normA = np.linalg.norm(A)

        for j in range(k):
            v = V[:, j]
            if np.allclose(v, 0):
                return False
            if lambdas is None:
                denom = np.vdot(v, v)
                if denom == 0:
                    return False
                lam = np.vdot(v, A @ v) / denom
            else:
                lam = lambdas[j]
            resid = A @ v - lam * v
            if np.linalg.norm(resid) > tol * (1.0 + normA):
                return False

        return True
