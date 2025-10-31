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
        # Expect problem to have 'points_src' and 'points_dst', each a list of 2D points
        points_src = np.array(problem['points_src'])
        points_dst = np.array(problem['points_dst'])
        n = points_src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build matrix A and vector b for least squares
        A = []
        b = []
        for i in range(n):
            x, y = points_src[i]
            xp, yp = points_dst[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(xp)
            b.append(yp)
        A = np.array(A)
        b = np.array(b)

        # Solve for affine parameters
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
        n = points_src.shape[0]
        # Apply affine transform to each src point and compare to dst
        src_hom = np.hstack([points_src, np.ones((n, 1))])  # shape (n, 3)
        transformed = (affine_matrix @ src_hom.T).T  # shape (n, 2)
        # Allow a small tolerance for floating point error
        return np.allclose(transformed, points_dst, atol=1e-6)
