import numpy as np


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.default_tolerance = 1e-6

    def _to_points_array(self, pts):
        arr = np.asarray(pts, dtype=float)
        if arr.ndim != 2 or arr.shape[1] != 2:
            raise ValueError("Points must be an array-like of shape (n, 2).")
        return arr

    def _compute_affine(self, src_points, dst_points, weights=None):
        src = self._to_points_array(src_points)
        dst = self._to_points_array(dst_points)
        n = src.shape[0]
        if dst.shape[0] != n:
            raise ValueError(
                "src_points and dst_points must have the same length.")
        if n == 0:
            A = np.eye(2)
            t = np.zeros(2)
            return A, t
        if n == 1:
            A = np.eye(2)
            t = dst[0] - src[0]
            return A, t
        M = np.zeros((2 * n, 6), dtype=float)
        b = np.zeros((2 * n,), dtype=float)
        for i, ((x, y), (X, Y)) in enumerate(zip(src, dst)):
            M[2 * i, 0:3] = [x, y, 1.0]
            M[2 * i, 3:6] = [0.0, 0.0, 0.0]
            b[2 * i] = X
            M[2 * i + 1, 0:3] = [0.0, 0.0, 0.0]
            M[2 * i + 1, 3:6] = [x, y, 1.0]
            b[2 * i + 1] = Y
        if weights is not None:
            w = np.asarray(weights, dtype=float).reshape(-1)
            if w.shape[0] != n:
                raise ValueError("weights must have same length as points.")
            W = np.repeat(w, 2)
            M = M * W[:, None]
            b = b * W
        params, _, _, _ = np.linalg.lstsq(M, b, rcond=None)
        a, b_, tx, c, d, ty = params
        A = np.array([[a, b_], [c, d]], dtype=float)
        t = np.array([tx, ty], dtype=float)
        return A, t

    def _invert_transform(self, A, t):
        A = np.asarray(A, dtype=float).reshape(2, 2)
        t = np.asarray(t, dtype=float).reshape(2)
        A_inv = np.linalg.inv(A)
        t_inv = -A_inv @ t
        return A_inv, t_inv

    def _apply(self, A, t, points):
        pts = self._to_points_array(points)
        A = np.asarray(A, dtype=float).reshape(2, 2)
        t = np.asarray(t, dtype=float).reshape(2)
        res = (pts @ A.T) + t
        return res

    def _round_points(self, pts, round_arg):
        if round_arg is True:
            return np.rint(pts).astype(int)
        if isinstance(round_arg, int):
            return np.round(pts, decimals=round_arg)
        return pts

    def _to_solution_dict(self, A, t, mapped_points=None):
        sol = {
            "matrix": [[float(A[0, 0]), float(A[0, 1])],
                       [float(A[1, 0]), float(A[1, 1])]],
            "translation": [float(t[0]), float(t[1])]
        }
        if mapped_points is not None:
            sol["mapped_points"] = [(float(p[0]), float(p[1]))
                                    for p in mapped_points]
        return sol

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        tol = float(problem.get("tolerance", self.default_tolerance))
        inverse = bool(problem.get("inverse", False))
        round_arg = problem.get("round", None)

        if "matrix" in problem and "translation" in problem:
            A = np.asarray(problem["matrix"], dtype=float).reshape(2, 2)
            t = np.asarray(problem["translation"], dtype=float).reshape(2)
        elif "src_points" in problem and "dst_points" in problem:
            A, t = self._compute_affine(
                problem["src_points"], problem["dst_points"], problem.get("weights"))
        else:
            A = np.eye(2)
            t = np.zeros(2)

        if inverse:
            A, t = self._invert_transform(A, t)

        mapped_points = None
        if "apply_points" in problem:
            mapped_points = self._apply(A, t, problem["apply_points"])
            mapped_points = self._round_points(mapped_points, round_arg)

        solution = self._to_solution_dict(A, t, mapped_points)

        if "return" in problem:
            mode = problem["return"]
            if mode == "transform":
                return {"matrix": solution["matrix"], "translation": solution["translation"]}
            if mode == "mapped_points":
                return solution.get("mapped_points", [])
        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        tol = float(problem.get("tolerance", self.default_tolerance))

        def get_transform(sol):
            if isinstance(sol, dict) and "matrix" in sol and "translation" in sol:
                A = np.asarray(sol["matrix"], dtype=float).reshape(2, 2)
                t = np.asarray(sol["translation"], dtype=float).reshape(2)
                return A, t
            return None, None

        def points_close(a, b, tolerance):
            a = np.asarray(a, dtype=float)
            b = np.asarray(b, dtype=float)
            if a.shape != b.shape:
                return False
            return np.allclose(a, b, atol=tolerance, rtol=0)

        # If ground truth expected mapping exists
        if isinstance(solution, dict) and "mapped_points" in solution and ("expected_mapped_points" in problem or "expected" in problem):
            expected = problem.get(
                "expected_mapped_points", problem.get("expected"))
            return points_close(solution["mapped_points"], expected, tol)

        A, t = get_transform(solution)
        if A is None or t is None:
            # If no transform provided but only mapped_points
            if isinstance(solution, dict) and "mapped_points" in solution and "apply_points" in problem:
                # Try derive transform from src/dst and validate mapped points
                if "src_points" in problem and "dst_points" in problem:
                    A_gt, t_gt = self._compute_affine(
                        problem["src_points"], problem["dst_points"], problem.get("weights"))
                    computed = self._apply(A_gt, t_gt, problem["apply_points"])
                    return points_close(solution["mapped_points"], computed, tol)
                # If expected is provided, compare directly
                if "expected_mapped_points" in problem or "expected" in problem:
                    expected = problem.get(
                        "expected_mapped_points", problem.get("expected"))
                    return points_close(solution["mapped_points"], expected, tol)
            return False

        # Validate that the transform fits provided point correspondences
        if "src_points" in problem and "dst_points" in problem:
            src = self._to_points_array(problem["src_points"])
            dst = self._to_points_array(problem["dst_points"])
            pred = self._apply(A, t, src)
            if not points_close(pred, dst, tol):
                return False

        # Validate mapped points if apply_points present
        if "apply_points" in problem:
            pred_map = self._apply(A, t, problem["apply_points"])
            if isinstance(solution, dict) and "mapped_points" in solution:
                if not points_close(pred_map, solution["mapped_points"], tol):
                    return False
            elif "expected_mapped_points" in problem or "expected" in problem:
                expected = problem.get(
                    "expected_mapped_points", problem.get("expected"))
                if not points_close(pred_map, expected, tol):
                    return False

        return True
