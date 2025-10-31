
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
                     Expected keys:
                         - 'src': list of [x, y] source points
                         - 'dst': list of [x', y'] destination points
        Returns:
            The solution in the format expected by the task:
                {'matrix': [[a, b, c], [d, e, f]]}
        '''
        src = problem.get('src')
        dst = problem.get('dst')

        if src is None or dst is None:
            raise ValueError("Problem must contain 'src' and 'dst' keys")

        src = np.asarray(src, dtype=float)
        dst = np.asarray(dst, dtype=float)

        if src.shape != dst.shape or src.ndim != 2 or src.shape[1] != 2:
            raise ValueError("Source and destination must be Nx2 arrays")

        n_points = src.shape[0]
        if n_points < 3:
            raise ValueError(
                "At least 3 points are required to determine an affine transform")

        # Build linear system A * params = b
        # params = [a, b, c, d, e, f]
        A = np.zeros((2 * n_points, 6), dtype=float)
        b = np.zeros((2 * n_points,), dtype=float)

        for i in range(n_points):
            x, y = src[i]
            x_prime, y_prime = dst[i]
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]
            b[2 * i] = x_prime
            b[2 * i + 1] = y_prime

        # Solve least squares (handles overdetermined systems)
        params, *_ = np.linalg.lstsq(A, b, rcond=None)
        matrix = params.reshape(2, 3).tolist()

        return {'matrix': matrix}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src = problem.get('src')
        dst = problem.get('dst')
        if src is None or dst is None:
            return False

        src = np.asarray(src, dtype=float)
        dst = np.asarray(dst, dtype=float)

        if src.shape != dst.shape or src.ndim != 2 or src.shape[1] != 2:
            return False

        matrix = solution.get('matrix')
        if matrix is None or len(matrix) != 2 or len(matrix[0]) != 3 or len(matrix[1]) != 3:
            return False

        # Convert to numpy array
        M = np.array(matrix, dtype=float)  # shape (2,3)

        # Apply affine transform: [x', y'] = [x, y, 1] @ M.T
        ones = np.ones((src.shape[0], 1), dtype=float)
        src_h = np.hstack([src, ones])  # shape (N,3)
        predicted = src_h @ M.T  # shape (N,2)

        # Compare with tolerance
        return np.allclose(predicted, dst, atol=1e-6, rtol=0)
