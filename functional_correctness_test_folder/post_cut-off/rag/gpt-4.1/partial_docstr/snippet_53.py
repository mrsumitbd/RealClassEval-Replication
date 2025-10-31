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
        # Expecting problem to have keys: 'source_points', 'target_points'
        src = np.array(problem['source_points'], dtype=float)
        tgt = np.array(problem['target_points'], dtype=float)
        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build matrix for least squares: [x y 1 0 0 0] [a b c d e f]^T = x'
        A = []
        B = []
        for (x, y), (xp, yp) in zip(src, tgt):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            B.append(xp)
            B.append(yp)
        A = np.array(A)
        B = np.array(B)
        params, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
        # params: [a, b, c, d, e, f]
        # Affine matrix:
        # [a b c]
        # [d e f]
        # [0 0 1]
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
        src = np.array(problem['source_points'], dtype=float)
        tgt = np.array(problem['target_points'], dtype=float)
        affine = np.array(solution, dtype=float)
        src_h = np.hstack([src, np.ones((src.shape[0], 1))])
        mapped = (affine @ src_h.T).T
        mapped = mapped[:, :2] / mapped[:, 2, np.newaxis]
        return np.allclose(mapped, tgt, atol=1e-6)
