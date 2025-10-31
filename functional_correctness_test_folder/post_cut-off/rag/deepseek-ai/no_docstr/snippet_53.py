
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
        for (x, y), (u, v) in zip(source_points, target_points):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(u)
            b.append(v)

        A = np.array(A)
        b = np.array(b)

        # Solve the least squares problem
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Extract the affine transformation matrix
        affine_matrix = params.reshape(2, 3)

        return {
            'affine_matrix': affine_matrix.tolist()
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            affine_matrix = np.array(solution['affine_matrix'])
            source_points = np.array(problem['source_points'])
            target_points = np.array(problem['target_points'])

            # Apply the affine transformation to source points
            transformed_points = []
            for x, y in source_points:
                transformed = np.dot(affine_matrix, [x, y, 1])
                transformed_points.append(transformed)

            transformed_points = np.array(transformed_points)

            # Check if transformed points are close to target points
            return np.allclose(transformed_points, target_points, atol=1e-6)
        except:
            return False
