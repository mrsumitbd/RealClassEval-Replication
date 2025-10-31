
class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.matrix = None

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Extract source and target points from the problem
        src_points = problem['source_points']
        tgt_points = problem['target_points']

        # Calculate the affine transformation matrix
        # The matrix is of the form:
        # [a, b, c]
        # [d, e, f]
        # where the transformation is given by:
        # x' = a*x + b*y + c
        # y' = d*x + e*y + f

        # We need at least 3 points to solve the system
        if len(src_points) < 3:
            raise ValueError(
                "At least 3 points are required to solve the affine transformation.")

        # Create the system of equations
        A = []
        B = []

        for (x, y), (xp, yp) in zip(src_points, tgt_points):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            B.append(xp)
            B.append(yp)

        # Solve the system using least squares
        import numpy as np
        A = np.array(A)
        B = np.array(B)
        self.matrix, _, _, _ = np.linalg.lstsq(A, B, rcond=None)

        # Reshape the matrix into the 2x3 affine transformation matrix
        self.matrix = self.matrix.reshape(2, 3)

        return self.matrix

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if solution.shape != (2, 3):
            return False

        src_points = problem['source_points']
        tgt_points = problem['target_points']

        for (x, y), (xp, yp) in zip(src_points, tgt_points):
            # Apply the affine transformation
            x_transformed = solution[0, 0] * x + \
                solution[0, 1] * y + solution[0, 2]
            y_transformed = solution[1, 0] * x + \
                solution[1, 1] * y + solution[1, 2]

            # Check if the transformed point matches the target point within a small tolerance
            if not (np.isclose(x_transformed, xp, atol=1e-6) and np.isclose(y_transformed, yp, atol=1e-6)):
                return False

        return True
