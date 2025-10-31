import numpy as np
from typing import Any


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        self.default_tol = 1e-7

    def _get_matrix(self, problem: dict) -> np.ndarray:
        A = problem.get('matrix', problem.get('A', None))
        if A is None:
            raise ValueError("Problem must contain 'matrix' or 'A'.")
        A = np.asarray(A, dtype=complex)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError('Matrix must be a square 2D array.')
        return A

    def _is_hermitian(self, A: np.ndarray, tol: float) -> bool:
        return np.allclose(A, A.conj().T, atol=tol, rtol=0.0)

    def _normalize_vectors(self, V: np.ndarray) -> np.ndarray:
        # V expected as (n, k) with eigenvectors as columns
        norms = np.linalg.norm(V, axis=0)
        norms[norms == 0] = 1.0
        return V / norms

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        A = self._get_matrix(problem)
        n = A.shape[0]
        tol = float(problem.get('tolerance', self.default_tol))
        right = bool(problem.get('right', True))
        normalize = bool(problem.get('normalize', True))
        sort_by = problem.get('sort', 'magnitude')
        descending = bool(problem.get('descending', False))
        num_pairs = problem.get('k', problem.get('num', None))
        if num_pairs is not None:
            num_pairs = int(num_pairs)
            if num_pairs < 1 or num_pairs > n:
                raise ValueError(
                    'Requested number of eigenpairs k must be between 1 and n.')
        hermitian = problem.get('hermitian', None)
        if hermitian is None:
            hermitian = self._is_hermitian(A, tol)

        # Choose matrix for computation based on right/left
        if right:
            A_eff = A
        else:
            # Left eigenvectors are eigenvectors of A^H with conjugate eigenvalues
            A_eff = A.conj().T

        if hermitian:
            vals, vecs = np.linalg.eigh(A_eff)
        else:
            vals, vecs = np.linalg.eig(A_eff)

        # If we computed for A^H (left), convert eigenvalues back to those of A
        if not right:
            vals = np.conj(vals)

        # Sorting
        if sort_by == 'magnitude':
            key = np.abs(vals)
        elif sort_by == 'real':
            key = np.real(vals)
        elif sort_by == 'imag':
            key = np.imag(vals)
        elif sort_by in ('value', 'lex'):
            key = np.lexsort((np.imag(vals), np.real(vals)))
            # When using lexsort, it returns indices directly
            order = key
            if descending:
                order = order[::-1]
            vals = vals[order]
            vecs = vecs[:, order]
            key = None  # prevent re-sorting below
        elif sort_by in ('none', None):
            key = None
        else:
            # Default to magnitude if unknown
            key = np.abs(vals)

        if key is not None:
            order = np.argsort(key)
            if descending:
                order = order[::-1]
            vals = vals[order]
            vecs = vecs[:, order]

        # Select top-k if requested
        if num_pairs is not None:
            vals = vals[:num_pairs]
            vecs = vecs[:, :num_pairs]

        if normalize:
            vecs = self._normalize_vectors(vecs)

        # Convert to serializable lists
        eigenvalues_list = [complex(v) for v in vals.tolist()]
        eigenvectors_list = [vecs[:, i].tolist() for i in range(vecs.shape[1])]

        return {
            'eigenvalues': eigenvalues_list,
            'eigenvectors': eigenvectors_list,
            'side': 'right' if right else 'left',
            'normalized': normalize,
            'sorted_by': sort_by,
            'hermitian': bool(hermitian),
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
        try:
            A = self._get_matrix(problem)
        except Exception:
            return False

        if not isinstance(solution, dict):
            return False

        vals = solution.get('eigenvalues', None)
        vecs = solution.get('eigenvectors', None)
        if vals is None or vecs is None:
            return False

        try:
            vals_arr = np.asarray(vals, dtype=complex)
        except Exception:
            return False
        if vals_arr.ndim != 1:
            return False

        # Accept vectors either as list of vectors (k, n) or (n, k)
        try:
            V = np.asarray(vecs, dtype=complex)
        except Exception:
            return False
        if V.ndim == 1:
            V = V.reshape(1, -1)  # single vector as row
        if V.ndim != 2:
            return False

        n = A.shape[0]
        # Determine orientation
        if V.shape[0] == len(vals_arr) and V.shape[1] == n:
            # shape (k, n) rows as vectors -> convert to columns (n, k)
            V = V.T
        elif V.shape[1] == len(vals_arr) and V.shape[0] == n:
            # already columns (n, k)
            pass
        else:
            return False

        k = V.shape[1]
        if len(vals_arr) != k:
            return False

        # Determine side
        right = problem.get('right', None)
        if right is None:
            side = solution.get('side', 'right')
            right = (str(side).lower() != 'left')

        tol = float(problem.get('tolerance', self.default_tol))
        # Use a slightly relaxed threshold in validation to account for serialization/rounding
        tol = max(tol, 1e-8)

        A_norm = np.linalg.norm(A)
        for i in range(k):
            lam = vals_arr[i]
            v = V[:, i]
            v_norm = np.linalg.norm(v)
            if v_norm == 0:
                return False
            if right:
                residual = A @ v - lam * v
            else:
                # Provided v is a left eigenvector (as column), check A^H v = conj(lam) v
                residual = A.conj().T @ v - np.conj(lam) * v
            res_norm = np.linalg.norm(residual)
            scale = (A_norm + abs(lam)) * v_norm + 1e-12
            if res_norm > tol * max(1.0, scale):
                return False

        return True
