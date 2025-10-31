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
        # Expecting problem to have 'source' and 'target' as lists of 2D points
        source = np.array(problem['source'])
        target = np.array(problem['target'])
        n = source.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build matrix A and vector b such that A x = b, where x contains the affine parameters
        # For each point: [x y 1 0 0 0] [a11 a12 tx]T = x'
        #                 [0 0 0 x y 1] [a21 a22 ty]T = y'
        A = np.zeros((2*n, 6))
        b = np.zeros((2*n,))
        for i in range(n):
            x, y = source[i]
            xp, yp = target[i]
            A[2*i, 0:3] = [x, y, 1]
            A[2*i+1, 3:6] = [x, y, 1]
            b[2*i] = xp
            b[2*i+1] = yp

        # Solve least squares
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        # params: [a11, a12, tx, a21, a22, ty]
        matrix = np.array([[params[0], params[1], params[2]],
                           [params[3], params[4], params[5]],
                           [0,         0,         1]])
        return matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # solution is expected to be a 3x3 matrix
        source = np.array(problem['source'])
        target = np.array(problem['target'])
        matrix = np.array(solution)
        n = source.shape[0]
        # Apply transform to source points
        src_h = np.hstack([source, np.ones((n, 1))])
        transformed = (matrix @ src_h.T).T
        transformed = transformed[:, :2] / transformed[:, 2:3]
        # Check if close to target
        return np.allclose(transformed, target, atol=1e-6)
