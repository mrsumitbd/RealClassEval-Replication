
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
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Extract source and target points from the problem
        source_points = problem['source_points']
        target_points = problem['target_points']

        # Calculate the affine transformation matrix
        # The matrix is of the form:
        # [a, b, c]
        # [d, e, f]
        # where (x', y') = (a*x + b*y + c, d*x + e*y + f)

        # We need at least 3 non-collinear points to solve for the matrix
        if len(source_points) < 3:
            raise ValueError(
                "At least 3 source points are required to solve for the affine transformation.")

        # Create the system of equations
        A = []
        B = []

        for (x, y), (x_p, y_p) in zip(source_points, target_points):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            B.append(x_p)
            B.append(y_p)

        # Solve the system of equations
        import numpy as np
        A = np.array(A)
        B = np.array(B)
        self.transformation_matrix, _, _, _ = np.linalg.lstsq(A, B, rcond=None)

        # Reshape the matrix into the 2x3 form
        self.transformation_matrix = self.transformation_matrix.reshape(2, 3)

        return {
            'transformation_matrix': self.transformation_matrix.tolist(),
            'source_points': source_points,
            'target_points': target_points
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
        if not isinstance(solution, dict):
            return False

        required_keys = ['transformation_matrix',
                         'source_points', 'target_points']
        if not all(key in solution for key in required_keys):
            return False

        # Check if the transformation matrix is valid
        matrix = solution['transformation_matrix']
        if not isinstance(matrix, list) or len(matrix) != 2 or any(len(row) != 3 for row in matrix):
            return False

        # Check if the source and target points are valid
        source_points = solution['source_points']
        target_points = solution['target_points']
        if not isinstance(source_points, list) or not isinstance(target_points, list):
            return False

        if len(source_points) != len(target_points):
            return False

        # Check if the points are in the correct format
        for points in [source_points, target_points]:
            for point in points:
                if not isinstance(point, (list, tuple)) or len(point) != 2:
                    return False
                if not all(isinstance(coord, (int, float)) for coord in point):
                    return False

        # Verify that the transformation matrix correctly maps source points to target points
        import numpy as np
        matrix = np.array(matrix)
        for (x, y), (x_p, y_p) in zip(source_points, target_points):
            transformed_x = matrix[0, 0] * x + matrix[0, 1] * y + matrix[0, 2]
            transformed_y = matrix[1, 0] * x + matrix[1, 1] * y + matrix[1, 2]
            if not np.isclose(transformed_x, x_p, atol=1e-6) or not np.isclose(transformed_y, y_p, atol=1e-6):
                return False

        return True
