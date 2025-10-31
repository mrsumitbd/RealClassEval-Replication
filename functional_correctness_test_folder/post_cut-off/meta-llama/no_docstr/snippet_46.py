
import numpy as np


class AffineTransform2D:

    def __init__(self):
        """
        Initialize an empty AffineTransform2D object.
        """
        self.matrix = np.eye(3)

    def solve(self, problem):
        """
        Solve for the affine transformation matrix given a problem.

        Args:
        problem (list of tuples): A list of three tuples, each containing two pairs of corresponding points.
                                  For example: [((x1, y1), (x1', y1')), ((x2, y2), (x2', y2')), ((x3, y3), (x3', y3'))]

        Returns:
        None
        """
        # Extract the points from the problem
        (x1, y1), (x1p, y1p) = problem[0]
        (x2, y2), (x2p, y2p) = problem[1]
        (x3, y3), (x3p, y3p) = problem[2]

        # Create the matrices for the system of linear equations
        A = np.array([[x1, y1, 1, 0, 0, 0],
                      [0, 0, 0, x1, y1, 1],
                      [x2, y2, 1, 0, 0, 0],
                      [0, 0, 0, x2, y2, 1],
                      [x3, y3, 1, 0, 0, 0],
                      [0, 0, 0, x3, y3, 1]])

        b = np.array([x1p, y1p, x2p, y2p, x3p, y3p])

        # Solve the system of linear equations
        try:
            params = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            raise ValueError(
                "The input points are not sufficient to determine a unique affine transformation.")

        # Store the affine transformation matrix
        self.matrix = np.array([[params[0], params[1], params[2]],
                                [params[3], params[4], params[5]],
                                [0, 0, 1]])

    def is_solution(self, problem, solution):
        """
        Check if a given solution is correct for the problem.

        Args:
        problem (list of tuples): A list of three tuples, each containing two pairs of corresponding points.
        solution (numpy array): A 3x3 numpy array representing the affine transformation matrix.

        Returns:
        bool: True if the solution is correct, False otherwise.
        """
        for (x, y), (xp, yp) in problem:
            transformed_point = np.dot(solution, np.array([x, y, 1]))
            if not np.allclose(transformed_point[:2], np.array([xp, yp])):
                return False
        return True
