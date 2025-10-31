
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.transform_matrix = None

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])

        A = []
        b = []

        for (x, y), (xp, yp) in zip(src_points, dst_points):
            A.extend([
                [x, y, 1, 0, 0, 0],
                [0, 0, 0, x, y, 1]
            ])
            b.extend([xp, yp])

        A = np.array(A)
        b = np.array(b)

        self.transform_matrix, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        return self.transform_matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        src_points = np.array(problem['src_points'])
        dst_points = np.array(problem['dst_points'])

        for (x, y), (xp, yp) in zip(src_points, dst_points):
            transformed_x = solution[0] * x + solution[1] * y + solution[2]
            transformed_y = solution[3] * x + solution[4] * y + solution[5]

            if not np.isclose(transformed_x, xp, atol=1e-6) or not np.isclose(transformed_y, yp, atol=1e-6):
                return False

        return True
