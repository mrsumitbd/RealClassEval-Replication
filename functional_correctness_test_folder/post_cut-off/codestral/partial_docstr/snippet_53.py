
class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.transformation_matrix = None

    def solve(self, problem):
        '''
        Solve the affine transformation problem.
        Args:
            problem: A dictionary containing the source and target points.
        Returns:
            The transformation matrix.
        '''
        source_points = problem['source_points']
        target_points = problem['target_points']

        # Calculate the transformation matrix
        # This is a simplified version and may not work for all cases
        # A more robust solution would be needed for a production environment
        A = []
        b = []
        for (x, y), (x_prime, y_prime) in zip(source_points, target_points):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.append(x_prime)
            b.append(y_prime)

        import numpy as np
        A = np.array(A)
        b = np.array(b)
        self.transformation_matrix, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        return self.transformation_matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        source_points = problem['source_points']
        target_points = problem['target_points']

        for (x, y), (x_prime, y_prime) in zip(source_points, target_points):
            transformed_x = solution[0] * x + solution[1] * y + solution[2]
            transformed_y = solution[3] * x + solution[4] * y + solution[5]

            if not np.isclose(transformed_x, x_prime) or not np.isclose(transformed_y, y_prime):
                return False

        return True
