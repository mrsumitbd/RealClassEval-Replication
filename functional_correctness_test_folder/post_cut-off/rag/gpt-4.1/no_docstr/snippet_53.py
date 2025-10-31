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

        # Build matrix A and vector b such that A x = b, where x are the affine parameters
        # Affine: [x', y', 1] = [x, y, 1] @ M.T, where M is 3x3, last row [0,0,1]
        # We solve for the 6 parameters of the 2x3 affine matrix
        A = []
        b = []
        for (x, y), (xp, yp) in zip(points_src, points_dst):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(xp)
            b.append(yp)
        A = np.array(A)
        b = np.array(b)
        # Least squares solution
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        # params: [a, b, c, d, e, f] for matrix [[a, b, c], [d, e, f]]
        affine_matrix = np.array([[params[0], params[1], params[2]],
                                  [params[3], params[4], params[5]]])
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
        # Add ones for homogeneous coordinates
        src_h = np.hstack([points_src, np.ones((points_src.shape[0], 1))])
        transformed = (affine_matrix @ src_h.T).T
        # Compare to points_dst
        return np.allclose(transformed, points_dst, atol=1e-6)
