
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
        X, residuals, rank, singular_values = np.linalg.lstsq(A, B, rcond=None)

        # Extract the transformation matrix
        self.transformation_matrix = np.array([
            [X[0], X[1], X[2]],
            [X[3], X[4], X[5]]
        ])

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
        if solution is None or not isinstance(solution, np.ndarray):
            return False

        if solution.shape != (2, 3):
            return False

        # Check if the solution transforms the source points to the target points within a small tolerance
        source_points = problem['source_points']
        target_points = problem['target_points']

        for (x, y), (x_p, y_p) in zip(source_points, target_points):
            transformed_x = solution[0, 0] * x + \
                solution[0, 1] * y + solution[0, 2]
            transformed_y = solution[1, 0] * x + \
                solution[1, 1] * y + solution[1, 2]

            if not np.isclose(transformed_x, x_p, atol=1e-6) or not np.isclose(transformed_y, y_p, atol=1e-6):
                return False

        return True
