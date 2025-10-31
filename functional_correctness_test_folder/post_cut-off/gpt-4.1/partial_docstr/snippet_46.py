
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
        Returns:
            The solution in the format expected by the task
        '''
        # problem: {'source': [[x1, y1], [x2, y2], ...], 'target': [[x1', y1'], [x2', y2'], ...]}
        src = np.array(problem['source'])
        tgt = np.array(problem['target'])
        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build matrix A and vector b for least squares
        # For each point: [x, y, 1, 0, 0, 0] * [a11, a12, tx] = x'
        #                 [0, 0, 0, x, y, 1] * [a21, a22, ty] = y'
        A = []
        b = []
        for i in range(n):
            x, y = src[i]
            xp, yp = tgt[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(xp)
            b.append(yp)
        A = np.array(A)
        b = np.array(b)
        # Solve for affine parameters
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        # params: [a11, a12, tx, a21, a22, ty]
        a11, a12, tx, a21, a22, ty = params
        # Return as a 2x3 matrix
        matrix = [[a11, a12, tx],
                  [a21, a22, ty]]
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
        src = np.array(problem['source'])
        tgt = np.array(problem['target'])
        matrix = np.array(solution['matrix'])  # shape (2,3)
        n = src.shape[0]
        # Apply affine transform to each source point
        src_h = np.hstack([src, np.ones((n, 1))])  # shape (n, 3)
        pred = (matrix @ src_h.T).T  # shape (n, 2)
        # Check if pred is close to tgt
        return np.allclose(pred, tgt, atol=1e-6)
