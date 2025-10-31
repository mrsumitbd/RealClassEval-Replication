
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
                {
                    "source": [[x1, y1], [x2, y2], [x3, y3], ...],
                    "target": [[x1', y1'], [x2', y2'], [x3', y3'], ...]
                }
        Returns:
            The solution in the format expected by the task:
                {
                    "matrix": [[a, b], [c, d]],
                    "offset": [e, f]
                }
            such that for each source point [x, y], the transformed point is:
                [x', y'] = [a, b; c, d] @ [x, y] + [e, f]
        '''
        src = np.array(problem['source'], dtype=np.float64)
        tgt = np.array(problem['target'], dtype=np.float64)
        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transformation.")

        # Build the system: for each point, [x', y'] = A @ [x, y] + t
        # We can write this as:
        # [x y 0 0 1 0] [a b c d e f]^T = x'
        # [0 0 x y 0 1] [a b c d e f]^T = y'
        # Stack for all points
        A = []
        B = []
        for i in range(n):
            x, y = src[i]
            xp, yp = tgt[i]
            A.append([x, y, 0, 0, 1, 0])
            A.append([0, 0, x, y, 0, 1])
            B.append(xp)
            B.append(yp)
        A = np.array(A)
        B = np.array(B)
        # Solve for [a, b, c, d, e, f]
        params, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
        a, b, c, d, e, f = params
        matrix = [[a, b], [c, d]]
        offset = [e, f]
        return {"matrix": matrix, "offset": offset}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        matrix = np.array(solution['matrix'], dtype=np.float64)
        offset = np.array(solution['offset'], dtype=np.float64)
        src = np.array(problem['source'], dtype=np.float64)
        tgt = np.array(problem['target'], dtype=np.float64)
        for i in range(src.shape[0]):
            transformed = matrix @ src[i] + offset
            if not np.allclose(transformed, tgt[i], atol=1e-6):
                return False
        return True
