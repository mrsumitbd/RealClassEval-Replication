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
        # Expect problem to have 'source_points' and 'target_points', each a list of (x, y)
        src = np.array(problem['source_points'])
        tgt = np.array(problem['target_points'])
        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine a 2D affine transform.")

        # Build matrix A and vector b such that A * params = b
        # params = [a, b, c, d, e, f] for affine: x' = a*x + b*y + c, y' = d*x + e*y + f
        A = []
        b = []
        for i in range(n):
            x, y = src[i]
            x_p, y_p = tgt[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(x_p)
            b.append(y_p)
        A = np.array(A)
        b = np.array(b)
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        # params: [a, b, c, d, e, f]
        solution = {
            'matrix': [[params[0], params[1]], [params[3], params[4]]],
            'offset': [params[2], params[5]]
        }
        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src = np.array(problem['source_points'])
        tgt = np.array(problem['target_points'])
        matrix = np.array(solution['matrix'])
        offset = np.array(solution['offset'])
        transformed = (src @ matrix.T) + offset
        return np.allclose(transformed, tgt, atol=1e-6)
