
class AffineTransform2D:

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Identity matrix

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Assuming problem contains 'points' and 'transformed_points'
        points = problem.get('points', [])
        transformed_points = problem.get('transformed_points', [])

        if len(points) != len(transformed_points) or len(points) < 3:
            raise ValueError("Insufficient data to solve the problem.")

        A = []
        B = []
        for (x, y), (x_prime, y_prime) in zip(points, transformed_points):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            B.append(x_prime)
            B.append(y_prime)

        import numpy as np
        A = np.array(A)
        B = np.array(B)
        solution = np.linalg.lstsq(A, B, rcond=None)[0]
        self.matrix = [
            [solution[0], solution[1], solution[2]],
            [solution[3], solution[4], solution[5]],
            [0, 0, 1]
        ]
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
        points = problem.get('points', [])
        transformed_points = problem.get('transformed_points', [])

        if len(points) != len(transformed_points):
            return False

        for (x, y), (x_prime, y_prime) in zip(points, transformed_points):
            x_transformed = solution[0][0] * x + \
                solution[0][1] * y + solution[0][2]
            y_transformed = solution[1][0] * x + \
                solution[1][1] * y + solution[1][2]
            if not (np.isclose(x_transformed, x_prime) and np.isclose(y_transformed, y_prime)):
                return False
        return True
