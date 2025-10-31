import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        self.default_tol = 1e-10

    def _to_array(self, X):
        if isinstance(X, np.ndarray):
            return X
        return np.asarray(X)

    def _is_square(self, X):
        return X.ndim == 2 and X.shape[0] == X.shape[1]

    def _symmetrize(self, X):
        if np.iscomplexobj(X):
            return (X + X.conj().T) / 2.0
        return (X + X.T) / 2.0

    def _check_finite(self, X):
        if not np.isfinite(X).all():
            raise ValueError("Input contains NaN or Inf.")

    def _project_psd(self, X, tol):
        S = self._symmetrize(X)
        # Use eigh for Hermitian matrices
        w, Q = np.linalg.eigh(S)
        w_clipped = np.maximum(w, 0.0)
        S_psd = (Q * w_clipped) @ Q.conj().T
        # Clean small imaginary parts for real inputs
        if not np.iscomplexobj(X):
            S_psd = S_psd.real
        rank = int(np.sum(w_clipped > tol))
        return S_psd, S, w, w_clipped, rank

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict.")

        # Accept multiple common keys
        X = problem.get('matrix', None)
        if X is None:
            X = problem.get('X', None)
        if X is None:
            X = problem.get('A', None)
        if X is None:
            raise KeyError(
                "Problem must contain a 'matrix' (or 'X'/'A') key with the input matrix.")

        X = self._to_array(X)
        if not self._is_square(X):
            raise ValueError("Input matrix must be square.")
        self._check_finite(X)

        tol = problem.get('tol', self.default_tol)

        projected, symmetric_input, eigenvalues, eigenvalues_clipped, rank = self._project_psd(
            X, tol)

        return {
            'projected_matrix': projected,
            'symmetric_input': symmetric_input,
            'eigenvalues': eigenvalues,
            'eigenvalues_clipped': eigenvalues_clipped,
            'rank': rank,
            'tol': tol,
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
        if solution is None:
            return False

        # Compute expected projection
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        tol = expected.get('tol', self.default_tol)
        rtol = max(1e-12, tol)
        atol = tol

        # Extract provided matrix
        if isinstance(solution, dict):
            sol_matrix = solution.get('projected_matrix', None)
            if sol_matrix is None:
                return False
        else:
            sol_matrix = solution

        try:
            sol_matrix = self._to_array(sol_matrix)
        except Exception:
            return False

        if not self._is_square(sol_matrix):
            return False

        # Check closeness to expected projection
        if not np.allclose(sol_matrix, expected['projected_matrix'], rtol=rtol, atol=atol):
            return False

        # Additional validity: symmetry and PSD
        sym = self._symmetrize(sol_matrix)
        if not np.allclose(sym, sol_matrix, rtol=rtol, atol=atol):
            return False

        try:
            w, _ = np.linalg.eigh(sym)
        except np.linalg.LinAlgError:
            return False

        if np.any(w < -10 * tol):
            return False

        return True
