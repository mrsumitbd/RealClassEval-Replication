
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
        Given a problem dict with keys:
            'source': list of 2D points [[x1, y1], [x2, y2], ...]
            'target': list of 2D points [[x1', y1'], [x2', y2'], ...]
        Returns:
            A dict with keys 'A' (2x2 matrix) and 'b' (2D vector) such that:
            target ≈ source @ A.T + b
        '''
        source = np.array(problem['source'], dtype=np.float64)
        target = np.array(problem['target'], dtype=np.float64)
        n = source.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build the system: for each point, [x y 1] @ [a11 a12 b1; a21 a22 b2] = [x', y']
        # So, for all points, we can write:
        # [x1 y1 0  0 1 0]   [a11]
        # [0  0  x1 y1 0 1]  [a12]
        # [x2 y2 0  0 1 0]   [a21]
        # [0  0  x2 y2 0 1]  [a22]
        # ...                [b1 ]
        #                    [b2 ]
        # = [x1', y1', x2', y2', ...]
        X = np.zeros((2*n, 6))
        Y = np.zeros((2*n,))
        for i in range(n):
            x, y = source[i]
            x_p, y_p = target[i]
            X[2*i,   0:2] = [x, y]
            X[2*i,   4] = 1
            X[2*i+1, 2:4] = [x, y]
            X[2*i+1, 5] = 1
            Y[2*i] = x_p
            Y[2*i+1] = y_p

        # Solve least squares
        params, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        A = np.array([[params[0], params[1]],
                      [params[2], params[3]]])
        b = np.array([params[4], params[5]])
        return {'A': A, 'b': b}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        source = np.array(problem['source'], dtype=np.float64)
        target = np.array(problem['target'], dtype=np.float64)
        A = np.array(solution['A'], dtype=np.float64)
        b = np.array(solution['b'], dtype=np.float64)
        transformed = (source @ A.T) + b
        # Allow a small tolerance for floating point errors
        return np.allclose(transformed, target, atol=1e-6)
