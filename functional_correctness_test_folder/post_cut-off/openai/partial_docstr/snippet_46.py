
import numpy as np


class AffineTransform2D:
    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
                     Expected keys:
                         - 'src': list of (x, y) tuples (source points)
                         - 'dst': list of (x, y) tuples (destination points)
        Returns:
            A dictionary with key 'matrix' containing the 2x3 affine transformation matrix
            as a list of lists: [[a, b, c], [d, e, f]]
        '''
        src = problem.get('src')
        dst = problem.get('dst')
        if src is None or dst is None:
            raise ValueError("Problem must contain 'src' and 'dst' keys.")
        if len(src) != len(dst):
            raise ValueError(
                "'src' and 'dst' must have the same number of points.")
        n = len(src)
        if n < 3:
            raise ValueError(
                "At least 3 point correspondences are required to determine an affine transform.")

        # Build the linear system A * params = b
        A = np.zeros((2 * n, 6))
        b = np.zeros((2 * n,))
        for i, ((x, y), (xp, yp)) in enumerate(zip(src, dst)):
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]
            b[2 * i] = xp
            b[2 * i + 1] = yp

        # Solve using least squares
        params, *_ = np.linalg.lstsq(A, b, rcond=None)
        a, b_, c, d, e, f = params
        matrix = [[a, b_, c], [d, e, f]]
        return {'matrix': matrix}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution dictionary (as returned by solve)
        Returns:
            True if the solution is valid within a tolerance, False otherwise
        '''
        src = problem.get('src')
        dst = problem.get('dst')
        if src is None or dst is None:
            return False
        if len(src) != len(dst):
            return False
        matrix = solution.get('matrix')
        if matrix is None or len(matrix) != 2 or len(matrix[0]) != 3 or len(matrix[1]) != 3:
            return False
        a, b_, c = matrix[0]
        d, e, f = matrix[1]
        tol = 1e-6
        for (x, y), (xp, yp) in zip(src, dst):
            x_pred = a * x + b_ * y + c
            y_pred = d * x + e * y + f
            if abs(x_pred - xp) > tol or abs(y_pred - yp) > tol:
                return False
        return True
