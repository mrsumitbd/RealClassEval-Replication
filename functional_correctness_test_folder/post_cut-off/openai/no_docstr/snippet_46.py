
import numpy as np


class AffineTransform2D:
    def __init__(self):
        # The affine transform will be stored as a 3x3 homogeneous matrix
        self.matrix = None

    def solve(self, problem):
        """
        Compute the affine transform that maps the source points to the destination points.

        Parameters
        ----------
        problem : dict
            Must contain two keys:
                'src' : list of (x, y) tuples (source points)
                'dst' : list of (x, y) tuples (destination points)

        Returns
        -------
        np.ndarray
            3x3 homogeneous affine transformation matrix.
        """
        src = np.asarray(problem['src'], dtype=float)
        dst = np.asarray(problem['dst'], dtype=float)

        if src.shape != dst.shape:
            raise ValueError(
                "Source and destination point sets must have the same shape")

        n = src.shape[0]
        if n < 3:
            raise ValueError(
                "At least 3 points are required to determine an affine transform")

        # Build the linear system M * params = b
        # params = [a, b, c, d, tx, ty] where the affine matrix is:
        # [[a, b, tx],
        #  [c, d, ty],
        #  [0, 0,  1]]
        M = np.zeros((2 * n, 6))
        b = np.zeros(2 * n)

        for i in range(n):
            x, y = src[i]
            x_prime, y_prime = dst[i]
            M[2 * i] = [x, y, 0, 0, 1, 0]
            M[2 * i + 1] = [0, 0, x, y, 0, 1]
            b[2 * i] = x_prime
            b[2 * i + 1] = y_prime

        # Solve using least squares
        params, *_ = np.linalg.lstsq(M, b, rcond=None)
        a, b_, c, d, tx, ty = params

        # Construct homogeneous matrix
        self.matrix = np.array([[a, b_, tx],
                                [c, d, ty],
                                [0, 0, 1]], dtype=float)
        return self.matrix

    def is_solution(self, problem, solution=None, atol=1e-6, rtol=1e-6):
        """
        Verify that the provided solution maps the source points to the destination points.

        Parameters
        ----------
        problem : dict
            Must contain 'src' and 'dst' as in solve().
        solution : np.ndarray, optional
            3x3 homogeneous affine matrix. If None, uses the stored self.matrix.
        atol : float
            Absolute tolerance for comparison.
        rtol : float
            Relative tolerance for comparison.

        Returns
        -------
        bool
            True if the solution is valid within the given tolerances.
        """
        if solution is None:
            if self.matrix is None:
                raise ValueError("No solution has been computed yet.")
            solution = self.matrix

        src = np.asarray(problem['src'], dtype=float)
        dst = np.asarray(problem['dst'], dtype=float)

        # Convert src to homogeneous coordinates
        ones = np.ones((src.shape[0], 1))
        src_h = np.hstack([src, ones])

        # Apply transform
        transformed = (solution @ src_h.T).T
        # Drop the homogeneous coordinate
        transformed = transformed[:, :2] / transformed[:, 2][:, np.newaxis]

        return np.allclose(transformed, dst, atol=atol, rtol=rtol)
