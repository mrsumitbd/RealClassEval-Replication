
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
        source_points = np.array(problem['source_points'])
        target_points = np.array(problem['target_points'])

        # Construct the matrix A and vector b for the least squares problem
        n = source_points.shape[0]
        A = np.zeros((2 * n, 6))
        b = np.zeros(2 * n)

        for i in range(n):
            x, y = source_points[i]
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]
            b[2 * i] = target_points[i, 0]
            b[2 * i + 1] = target_points[i, 1]

        # Solve the least squares problem
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Extract the affine transformation matrix and translation vector
        a, b, c, d, e, f = params
        transform_matrix = np.array([[a, b], [d, e]])
        translation_vector = np.array([c, f])

        solution = {
            'transform_matrix': transform_matrix.tolist(),
            'translation_vector': translation_vector.tolist()
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
        transform_matrix = np.array(solution['transform_matrix'])
        translation_vector = np.array(solution['translation_vector'])

        for i in range(len(source_points)):
            transformed_point = np.dot(
                transform_matrix, source_points[i]) + translation_vector
            if not np.allclose(transformed_point, target_points[i], atol=1e-6):
                return False
        return True
