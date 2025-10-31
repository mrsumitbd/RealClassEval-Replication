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
        # Expecting problem to have 'points_src' and 'points_dst', each a list of 2D points
        points_src = np.array(problem['points_src'])
        points_dst = np.array(problem['points_dst'])
        n = points_src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build matrix A and vector b such that A x = b, where x is the flattened affine matrix
        # Affine: [a b tx; c d ty]
        A = []
        b = []
        for (x, y), (xp, yp) in zip(points_src, points_dst):
            A.append([x, y, 0, 0, 1, 0])
            A.append([0, 0, x, y, 0, 1])
            b.append(xp)
            b.append(yp)
        A = np.array(A)
        b = np.array(b)
        # Solve for affine parameters
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        # params: [a, b, c, d, tx, ty]
        affine_matrix = np.array([
            [params[0], params[1], params[4]],
            [params[2], params[3], params[5]],
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
        points_src = np.array(problem['points_src'])
        points_dst = np.array(problem['points_dst'])
        affine_matrix = np.array(solution)
        # Convert points_src to homogeneous coordinates
        ones = np.ones((points_src.shape[0], 1))
        src_hom = np.hstack([points_src, ones])
        # Apply affine transformation
        dst_pred = (affine_matrix @ src_hom.T).T
        dst_pred = dst_pred[:, :2] / dst_pred[:, 2][:, None]
        # Check if close to points_dst
        return np.allclose(dst_pred, points_dst, atol=1e-6)
