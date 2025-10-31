
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
                     Expected key: 'A' – a square complex numpy array.
        Returns:
            A dictionary with keys:
                'eigenvalues' : 1-D array of eigenvalues
                'eigenvectors': 2-D array whose columns are the corresponding eigenvectors
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dictionary")
        if 'A' not in problem:
            raise KeyError("problem dictionary must contain key 'A'")
        A = problem['A']
        if not isinstance(A, np.ndarray):
            raise TypeError("'A' must be a numpy.ndarray")
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'A' must be a square matrix")
        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(A.astype(complex))
        return {'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary (must contain 'A')
            solution: The proposed solution dictionary (must contain 'eigenvalues' and 'eigenvectors')
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Basic validation of inputs
        if not isinstance(problem, dict) or not isinstance(solution, dict):
            return False
        if 'A' not in problem or 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False

        A = problem['A']
        try:
            true_vals, true_vecs = np.linalg.eig(A.astype(complex))
        except Exception:
            return False

        sol_vals = solution['eigenvalues']
        sol_vecs = solution['eigenvectors']

        # Check shapes
        if sol_vals.shape != true_vals.shape:
            return False
        if sol_vecs.shape != true_vecs.shape:
            return False

        # Sort eigenvalues and corresponding vectors for comparison
        # Use a tolerance for eigenvalue equality
        tol = 1e-6

        # Create a mapping from true eigenvalues to their vectors
        true_pairs = []
        for val, vec in zip(true_vals, true_vecs.T):
            true_pairs.append((val, vec))
        # Sort by eigenvalue magnitude to reduce matching ambiguity
        true_pairs.sort(key=lambda x: (np.abs(x[0]), np.angle(x[0])))
        true_vals_sorted = np.array([p[0] for p in true_pairs])
        true_vecs_sorted = np.column_stack([p[1] for p in true_pairs])

        # Similarly sort solution pairs
        sol_pairs = []
        for val, vec in zip(sol_vals, sol_vecs.T):
            sol_pairs.append((val, vec))
        sol_pairs.sort(key=lambda x: (np.abs(x[0]), np.angle(x[0])))
        sol_vals_sorted = np.array([p[0] for p in sol_pairs])
        sol_vecs_sorted = np.column_stack([p[1] for p in sol_pairs])

        # Compare eigenvalues within tolerance
        if not np.allclose(true_vals_sorted, sol_vals_sorted, atol=tol, rtol=tol):
            return False

        # For each pair, check if solution vector is a scalar multiple of true vector
        for true_vec, sol_vec in zip(true_vecs_sorted.T, sol_vecs_sorted.T):
            # Avoid zero vector
            if np.allclose(true_vec, 0, atol=tol):
                if not np.allclose(sol_vec, 0, atol=tol):
                    return False
                continue
            # Compute scaling factor that best aligns sol_vec to true_vec
            # Use least squares: sol_vec ≈ c * true_vec
            c = np.vdot(true_vec, sol_vec) / np.vdot(true_vec, true_vec)
            if not np.allclose(sol_vec, c * true_vec, atol=tol, rtol=tol):
                return False

        return True
