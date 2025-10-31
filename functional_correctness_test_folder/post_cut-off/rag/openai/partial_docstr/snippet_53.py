
import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        # No state needed for this simple implementation
        pass

    def _extract_points(self, problem):
        """
        Helper to extract source and destination points from the problem dict.
        Supports two common formats:
          - {'src': [...], 'dst': [...]}
          - {'points': [(src, dst), ...]}
        Returns:
            src_points: np.ndarray of shape (N, 2)
            dst_points: np.ndarray of shape (N, 2)
        Raises:
            ValueError if the format is unsupported or inconsistent.
        """
        if 'src' in problem and 'dst' in problem:
            src = np.asarray(problem['src'], dtype=float)
            dst = np.asarray(problem['dst'], dtype=float)
            if src.shape != dst.shape or src.ndim != 2 or src.shape[1] != 2:
                raise ValueError("src and dst must be arrays of shape (N, 2)")
            return src, dst
        elif 'points' in problem:
            pts = np.asarray(problem['points'], dtype=float)
            if pts.ndim != 3 or pts.shape[1] != 2 or pts.shape[2] != 2:
                raise ValueError("points must be array of shape (N, 2, 2)")
            src = pts[:, 0, :]
            dst = pts[:, 1, :]
            return src, dst
        else:
            raise ValueError(
                "Problem dict must contain 'src' and 'dst' or 'points'")

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
            (a 2x3 matrix as a list of lists)
        '''
        src, dst = self._extract_points(problem)
        N = src.shape[0]
        if N == 0:
            raise ValueError("No points provided")

        # Build design matrix M of shape (2N, 6)
        ones = np.ones((N, 1), dtype=float)
        M = np.hstack([src, ones])  # shape (N, 3)
        M = np.vstack([M, M])       # shape (2N, 3)
        # Repeat for y coordinates
        M[1::2, :] = M[0::2, :]     # duplicate rows for y equations

        # Build target vector b of shape (2N,)
        b = dst.reshape(-1)  # flatten to (2N,)

        # Solve least squares: M * params = b
        params, *_ = np.linalg.lstsq(M, b, rcond=None)
        # params shape (6,)
        # Reshape into 2x3 matrix
        transform = params.reshape(2, 3)
        # Convert to list of lists for output
        return transform.tolist()

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
            src, dst = self._extract_points(problem)
        except ValueError:
            return False

        # Convert solution to numpy array
        try:
            T = np.asarray(solution, dtype=float)
            if T.shape != (2, 3):
                return False
        except Exception:
            return False

        # Apply transform to src points
        ones = np.ones((src.shape[0], 1), dtype=float)
        src_h = np.hstack([src, ones])  # shape (N, 3)
        dst_pred = src_h @ T.T          # shape (N, 2)

        # Compute residuals
        diff = dst_pred - dst
        # Use a tolerance
        tol = 1e-6
        return np.all(np.abs(diff) <= tol)
