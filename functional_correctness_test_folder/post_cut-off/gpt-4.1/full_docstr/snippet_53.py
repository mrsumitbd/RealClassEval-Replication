
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Expecting problem to have 'source_points' and 'target_points'
        # Each is a list of 2D points: [[x1, y1], [x2, y2], ...]
        src = np.array(problem['source_points'], dtype=np.float64)
        tgt = np.array(problem['target_points'], dtype=np.float64)
        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transformation.")

        # Build matrix for least squares: [x y 1 0 0 0] [a11 a12 tx]T = x'
        #                                 [0 0 0 x y 1] [a21 a22 ty]T = y'
        A = []
        B = []
        for i in range(n):
            x, y = src[i]
            xp, yp = tgt[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            B.append(xp)
            B.append(yp)
        A = np.array(A)
        B = np.array(B)
        # Solve for affine parameters
        params, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
        # params: [a11, a12, tx, a21, a22, ty]
        affine_matrix = np.array([
            [params[0], params[1], params[2]],
            [params[3], params[4], params[5]],
            [0,         0,         1]
        ])
        return affine_matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src = np.array(problem['source_points'], dtype=np.float64)
        tgt = np.array(problem['target_points'], dtype=np.float64)
        n = src.shape[0]
        if solution.shape != (3, 3):
            return False
        # Apply affine transform to source points
        src_h = np.hstack([src, np.ones((n, 1))])  # (n, 3)
        transformed = (solution @ src_h.T).T  # (n, 3)
        transformed = transformed[:, :2] / transformed[:, 2][:, None]
        # Check if close to target points
        return np.allclose(transformed, tgt, atol=1e-6)
