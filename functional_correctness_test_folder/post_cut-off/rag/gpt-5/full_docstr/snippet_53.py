import numpy as np
from typing import Any, Dict, List, Tuple, Optional


class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            return None

        tol = float(problem.get("tolerance", 1e-8))
        round_outputs = bool(problem.get("round", False))

        # Case 1: Apply provided transform to provided points
        if "transform" in problem:
            A, b = self._normalize_transform(problem["transform"])
            solution: Dict[str, Any] = {
                "transform": {"A": A.tolist(), "b": b.tolist()}}

            # Apply to different possible keys
            if "points" in problem:
                pts = self._points_to_array(problem["points"])
                out = (pts @ A.T) + b
                if round_outputs:
                    out = np.rint(out).astype(int)
                solution["transformed_points"] = out.tolist()

            if "query" in problem:
                q = self._points_to_array(problem["query"])
                out_q = (q @ A.T) + b
                if round_outputs:
                    out_q = np.rint(out_q).astype(int)
                solution["transformed_query"] = out_q.tolist()

            # If src/dst present, compute residual to assess transform fit
            if "src" in problem and "dst" in problem:
                src = self._points_to_array(problem["src"])
                dst = self._points_to_array(problem["dst"])
                pred = (src @ A.T) + b
                residuals = np.linalg.norm(pred - dst, axis=1)
                solution["residuals"] = residuals.tolist()
                solution["max_error"] = float(
                    np.max(residuals)) if residuals.size else 0.0
                solution["mean_error"] = float(
                    np.mean(residuals)) if residuals.size else 0.0
                solution["valid"] = bool(np.all(residuals <= tol))

            return solution

        # Case 2: Estimate transform from src->dst. Optionally transform query/points.
        if "src" in problem and "dst" in problem:
            src = self._points_to_array(problem["src"])
            dst = self._points_to_array(problem["dst"])
            A, b = self._estimate_affine(src, dst)
            solution = {"transform": {"A": A.tolist(), "b": b.tolist()}}

            # Evaluate fit
            pred = (src @ A.T) + b
            residuals = np.linalg.norm(pred - dst, axis=1)
            solution["residuals"] = residuals.tolist()
            solution["max_error"] = float(
                np.max(residuals)) if residuals.size else 0.0
            solution["mean_error"] = float(
                np.mean(residuals)) if residuals.size else 0.0
            solution["valid"] = bool(np.all(residuals <= tol))

            # Apply to query or points if provided
            if "query" in problem:
                q = self._points_to_array(problem["query"])
                out_q = (q @ A.T) + b
                if round_outputs:
                    out_q = np.rint(out_q).astype(int)
                solution["transformed_query"] = out_q.tolist()

            if "points" in problem:
                pts = self._points_to_array(problem["points"])
                out_pts = (pts @ A.T) + b
                if round_outputs:
                    out_pts = np.rint(out_pts).astype(int)
                solution["transformed_points"] = out_pts.tolist()

            # Also include transformed_src as a convenience for validation
            solution["transformed_src"] = pred.tolist()
            return solution

        # Fallback: if points exist but no transform, return identity mapping result
        if "points" in problem:
            pts = self._points_to_array(problem["points"])
            if round_outputs:
                pts = np.rint(pts).astype(int)
            return {"transform": {"A": np.eye(2).tolist(), "b": [0.0, 0.0]},
                    "transformed_points": pts.tolist(),
                    "valid": True}

        return None

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(problem, dict) or not isinstance(solution, dict):
            return False

        tol = float(problem.get("tolerance", 1e-8))

        # Priority 1: If problem specifies src/dst, verify mapping
        if "src" in problem and "dst" in problem:
            src = self._points_to_array(problem["src"])
            dst = self._points_to_array(problem["dst"])

            # If solution provides a transform, use it to check
            if "transform" in solution:
                try:
                    A, b = self._normalize_transform(solution["transform"])
                except Exception:
                    return False
                pred = (src @ A.T) + b
                return bool(np.allclose(pred, dst, atol=tol))

            # Else if solution provides transformed_src, compare that to dst
            if "transformed_src" in solution:
                pred = self._points_to_array(solution["transformed_src"])
                return bool(np.allclose(pred, dst, atol=tol))

            return False

        # Priority 2: If problem specifies expected/target for transformed points
        expected_keys = ["expected_points",
                         "target_points", "expected", "target"]
        solution_keys = ["transformed_points", "result", "output"]
        for ek in expected_keys:
            if ek in problem:
                expected = problem[ek]
                exp_arr = self._points_to_array(expected)
                for sk in solution_keys:
                    if sk in solution:
                        got_arr = self._points_to_array(solution[sk])
                        if got_arr.shape == exp_arr.shape and np.allclose(got_arr, exp_arr, atol=tol):
                            return True
                return False

        # Priority 3: If query mapping is specified
        if "query" in problem:
            expected_query_keys = [
                "expected_query", "target_query", "expected_query_points", "target_query_points"]
            for ek in expected_query_keys:
                if ek in problem:
                    exp_q = self._points_to_array(problem[ek])
                    if "transformed_query" in solution:
                        got_q = self._points_to_array(
                            solution["transformed_query"])
                        return bool(got_q.shape == exp_q.shape and np.allclose(got_q, exp_q, atol=tol))
                    # If we have transform, try to compute and check
                    if "transform" in solution:
                        A, b = self._normalize_transform(solution["transform"])
                        q = self._points_to_array(problem["query"])
                        pred_q = (q @ A.T) + b
                        return bool(pred_q.shape == exp_q.shape and np.allclose(pred_q, exp_q, atol=tol))
                    return False

        # If no validation criteria available, consider invalid
        return False

    def _points_to_array(self, pts: Any) -> np.ndarray:
        arr = np.asarray(pts, dtype=float)
        if arr.ndim == 1:
            if arr.size == 2:
                arr = arr.reshape(1, 2)
            else:
                raise ValueError("Points must be of shape (N,2) or (2,).")
        if arr.shape[-1] != 2:
            raise ValueError("Points must have last dimension of size 2.")
        return arr

    def _normalize_transform(self, transform: Any) -> Tuple[np.ndarray, np.ndarray]:
        # Accept dict with A and b
        if isinstance(transform, dict):
            if "A" in transform and "b" in transform:
                A = np.asarray(transform["A"], dtype=float)
                b = np.asarray(transform["b"], dtype=float).reshape(2)
                if A.shape != (2, 2) or b.shape != (2,):
                    raise ValueError(
                        "Transform dict must have A (2x2) and b (2,).")
                return A, b

            # Accept "M" 3x3 homogeneous
            if "M" in transform:
                M = np.asarray(transform["M"], dtype=float)
                if M.shape != (3, 3):
                    raise ValueError("Homogeneous matrix M must be 3x3.")
                A = M[:2, :2]
                b = M[:2, 2]
                return A, b

        # Accept list/array of length 6: [a11, a12, a21, a22, tx, ty]
        arr = np.asarray(transform, dtype=float).ravel()
        if arr.size == 6:
            A = np.array([[arr[0], arr[1]], [arr[2], arr[3]]], dtype=float)
            b = np.array([arr[4], arr[5]], dtype=float)
            return A, b

        # Accept 3x3 matrix directly
        if arr.size == 9:
            M = arr.reshape(3, 3)
            A = M[:2, :2]
            b = M[:2, 2]
            return A, b

        raise ValueError(
            "Unsupported transform format. Provide {'A':2x2,'b':2}, 6-vector, or 3x3 'M'.")

    def _estimate_affine(self, src: np.ndarray, dst: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        if src.shape != dst.shape or src.ndim != 2 or src.shape[1] != 2:
            raise ValueError("src and dst must be of shape (N,2) and equal.")

        n = src.shape[0]
        if n == 0:
            # Degenerate: return identity
            return np.eye(2), np.zeros(2)

        # Build linear system
        # For each (x,y)->(u,v):
        # [x y 0 0 1 0] [a11 a12 a21 a22 tx ty]^T = u
        # [0 0 x y 0 1] [...] = v
        A_mat = np.zeros((2 * n, 6), dtype=float)
        b_vec = np.zeros((2 * n,), dtype=float)

        A_mat[0::2, 0] = src[:, 0]
        A_mat[0::2, 1] = src[:, 1]
        A_mat[0::2, 4] = 1.0
        b_vec[0::2] = dst[:, 0]

        A_mat[1::2, 2] = src[:, 0]
        A_mat[1::2, 3] = src[:, 1]
        A_mat[1::2, 5] = 1.0
        b_vec[1::2] = dst[:, 1]

        # Solve least squares
        params, _, _, _ = np.linalg.lstsq(A_mat, b_vec, rcond=None)
        a11, a12, a21, a22, tx, ty = params.tolist()
        A = np.array([[a11, a12], [a21, a22]], dtype=float)
        b = np.array([tx, ty], dtype=float)
        return A, b
