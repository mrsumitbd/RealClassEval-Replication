
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
        source_points = np.array(problem['source_points'])
        target_points = np.array(problem['target_points'])

        # Construct the matrix A and vector b for the least squares problem
        A = []
        b = []
        for i in range(len(source_points)):
            x, y = source_points[i]
            u, v = target_points[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(u)
            b.append(v)

        A = np.array(A)
        b = np.array(b)

        # Solve the least squares problem
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Extract the affine transformation matrix and translation vector
        a, b, c, d, e, f = params
        affine_matrix = [[a, b], [d, e]]
        translation = [c, f]

        solution = {
            'affine_matrix': affine_matrix,
            'translation': translation
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
        source_points = np.array(problem['source_points'])
        target_points = np.array(problem['target_points'])
        affine_matrix = np.array(solution['affine_matrix'])
        translation = np.array(solution['translation'])

        for i in range(len(source_points)):
            x, y = source_points[i]
            transformed = np.dot(affine_matrix, [x, y]) + translation
            expected = target_points[i]
            if not np.allclose(transformed, expected, atol=1e-6):
                return False
        return True
