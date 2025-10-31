
import numpy as np


class AffineTransform2D:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Solves for the affine transformation matrix that maps points from the source to the target.

        Args:
            problem: A dictionary with keys 'source' and 'target', each containing a list of 3 (x, y) points.

        Returns:
            A 3x3 numpy array representing the affine transformation matrix.
        """
        source = np.array(problem['source'])
        target = np.array(problem['target'])

        # Construct the matrix A and vector b for the system Ax = b
        A = []
        b = []
        for i in range(3):
            x, y = source[i]
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            b.extend(target[i])

        A = np.array(A)
        b = np.array(b)

        # Solve the linear system
        x = np.linalg.lstsq(A, b, rcond=None)[0]

        # Construct the transformation matrix
        transform = np.array([
            [x[0], x[1], x[2]],
            [x[3], x[4], x[5]],
            [0, 0, 1]
        ])

        return transform

    def is_solution(self, problem, solution):
        """
        Checks if the solution correctly transforms the source points to the target points.

        Args:
            problem: A dictionary with keys 'source' and 'target', each containing a list of 3 (x, y) points.
            solution: A 3x3 numpy array representing the affine transformation matrix.

        Returns:
            True if the solution is correct within a small tolerance, False otherwise.
        """
        source = np.array(problem['source'])
        target = np.array(problem['target'])

        # Apply the transformation to the source points
        transformed = []
        for point in source:
            homogeneous = np.array([point[0], point[1], 1])
            transformed_point = solution @ homogeneous
            transformed.append(transformed_point[:2])
        transformed = np.array(transformed)

        # Check if the transformed points match the target points
        return np.allclose(transformed, target, atol=1e-6)
