
import numpy as np


class AffineTransform2D:
    """
    Solves for a 2‑D affine transformation that maps a set of source points
    to a set of destination points.

    The transformation is represented by the 3×3 matrix

        [[a, b, c],
         [d, e, f],
         [0, 0, 1]]

    which acts on homogeneous coordinates [x, y, 1]ᵀ.
    """

    def __init__(self):
        """No state is required for this solver."""
        pass

    def solve(self, problem):
        """
        Compute the affine transformation parameters.

        Parameters
        ----------
        problem : dict
            Must contain two keys:
                'src' : list of (x, y) tuples (source points)
                'dst' : list of (x', y') tuples (destination points)

            At least three point correspondences are required.

        Returns
        -------
        numpy.ndarray
            A 6‑element vector [a, b, c, d, e, f] that defines the affine
            transformation.

        Raises
        ------
        ValueError
            If the input dictionary is malformed or contains fewer than
            three correspondences.
        """
        if not isinstance(problem, dict):
            raise ValueError(
                "Problem must be a dictionary with 'src' and 'dst' keys.")

        src = problem.get('src')
        dst = problem.get('dst')

        if src is None or dst is None:
            raise ValueError(
                "Problem dictionary must contain 'src' and 'dst' keys.")
        if len(src) != len(dst):
            raise ValueError(
                "'src' and 'dst' must have the same number of points.")
        if len(src) < 3:
            raise ValueError(
                "At least three point correspondences are required.")

        n = len(src)
        A = np.zeros((2 * n, 6))
        b = np.zeros(2 * n)

        for i, ((x, y), (xp, yp)) in enumerate(zip(src, dst)):
            A[2 * i] = [x, y, 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, x, y, 1]
            b[2 * i] = xp
            b[2 * i + 1] = yp

        # Solve the least‑squares problem
        sol, *_ = np.linalg.lstsq(A, b, rcond=None)
        return sol

    def is_solution(self, problem, solution, atol=1e-6, rtol=1e-6):
        """
        Verify that a given solution maps the source points to the destination
        points within a specified tolerance.

        Parameters
        ----------
        problem : dict
            Same format as accepted by `solve`.
        solution : array‑like
            6‑element vector [a, b, c, d, e, f].
        atol : float, optional
            Absolute tolerance.
        rtol : float, optional
            Relative tolerance.

        Returns
        -------
        bool
            True if the transformation maps all source points to the
            corresponding destination points within the tolerance.
        """
        if solution is None:
            return False
        sol = np.asarray(solution, dtype=float)
        if sol.shape != (6,):
            return False

        a, b, c, d, e, f = sol
        src = problem.get('src')
        dst = problem.get('dst')
        if src is None or dst is None or len(src) != len(dst):
            return False

        for (x, y), (xp, yp) in zip(src, dst):
            x_mapped = a * x + b * y + c
            y_mapped = d * x + e * y + f
            if not (np.isclose(x_mapped, xp, atol=atol, rtol=rtol) and
                    np.isclose(y_mapped, yp, atol=atol, rtol=rtol)):
                return False
        return True
