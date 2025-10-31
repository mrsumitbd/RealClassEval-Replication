import math
from typing import Any, Iterable, Sequence

import numpy as np


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
            raise TypeError("problem must be a dict")

        tol = float(problem.get("tolerance", 1e-9))
        do_inverse = bool(problem.get("inverse", False))
        round_decimals = problem.get("round", None)
        to_int = problem.get("dtype", None) in ("int", int, "i", "integer")

        # Determine transformation matrix
        T = None

        # Option 1: estimate from correspondences
        if ("source_points" in problem or "src_points" in problem) and (
            "target_points" in problem or "dst_points" in problem
        ):
            src = problem.get("source_points", problem.get("src_points"))
            dst = problem.get("target_points", problem.get("dst_points"))
            src_pts = self._parse_points(src)
            dst_pts = self._parse_points(dst)
            T = self._estimate_affine(src_pts, dst_pts, tol=tol)

        # Option 2: from provided matrix/translation
        if T is None:
            matrix = (
                problem.get("affine")
                or problem.get("matrix")
                or problem.get("A")
                or problem.get("M")
            )
            translation = problem.get("translation") or problem.get("t")
            if matrix is not None or translation is not None:
                T = self._to_homogeneous_matrix(matrix, translation)

        # Option 3: from sequence of primitive transforms
        if T is None and "transforms" in problem:
            T = self._compose_from_operations(problem["transforms"])

        # Fallback: identity if nothing specified
        if T is None:
            T = np.eye(3, dtype=float)

        # Optional: invert
        if do_inverse:
            T = np.linalg.inv(T)

        # Apply to points if provided
        transformed_points = None
        if "points" in problem:
            points = self._parse_points(problem["points"])
            transformed_points = self._apply(T, points)
        elif "x" in problem and "y" in problem:
            # Support separate coordinate arrays
            x = np.asarray(problem["x"], dtype=float)
            y = np.asarray(problem["y"], dtype=float)
            pts = np.stack([x.ravel(), y.ravel()], axis=1)
            out = self._apply(T, pts)
            transformed_points = out.reshape(*x.shape, 2).tolist()

        # Rounding / dtype conversion
        if transformed_points is not None:
            arr = np.asarray(transformed_points, dtype=float)
            if round_decimals is not None:
                arr = np.round(arr, int(round_decimals))
            if to_int:
                arr = np.rint(arr).astype(int)
            transformed_points = arr.tolist()

        # Build solution dictionary
        solution = {
            "matrix": T.tolist(),
        }
        if transformed_points is not None:
            solution["transformed_points"] = transformed_points

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
        if not isinstance(problem, dict):
            return False

        tol = float(problem.get("tolerance", 1e-6))

        # If solution is just a list of points, wrap it
        if isinstance(solution, (list, tuple)):
            solution = {"transformed_points": solution}
        if not isinstance(solution, dict):
            return False

        # Recompute expected using solve (without modifying original problem)
        expected = self.solve(problem)

        # Compare transformed points if present in provided solution or problem expects points
        if "points" in problem or "transformed_points" in solution:
            if "transformed_points" not in solution or "transformed_points" not in expected:
                return False
            a = np.asarray(solution["transformed_points"], dtype=float)
            b = np.asarray(expected["transformed_points"], dtype=float)
            if a.shape != b.shape:
                return False
            if not np.allclose(a, b, atol=tol, rtol=0):
                return False

        # If matrix provided, also compare matrices (up to scale 1 factor not allowed; affine is exact)
        if "matrix" in solution:
            aM = np.asarray(solution["matrix"], dtype=float)
            eM = np.asarray(expected["matrix"], dtype=float)
            if aM.shape != (3, 3) or eM.shape != (3, 3):
                return False
            if not np.allclose(aM, eM, atol=tol, rtol=0):
                return False

        return True

    # ----------------- Helpers -----------------

    @staticmethod
    def _parse_points(points: Any) -> np.ndarray:
        if isinstance(points, np.ndarray):
            arr = points
        else:
            arr = np.asarray(points)
        if arr.size == 0:
            return arr.reshape(0, 2).astype(float)
        if arr.ndim == 1 and arr.shape[0] == 2:
            arr = arr.reshape(1, 2)
        if arr.ndim != 2 or arr.shape[1] != 2:
            raise ValueError("points must be Nx2")
        return arr.astype(float)

    @staticmethod
    def _to_homogeneous_matrix(matrix: Any, translation: Any) -> np.ndarray:
        # Accept various forms:
        # - 3x3 full matrix
        # - 2x3 affine block
        # - 2x2 with translation vector
        if matrix is None and translation is None:
            return np.eye(3, dtype=float)

        if matrix is not None:
            M = np.asarray(matrix, dtype=float)
            if M.shape == (3, 3):
                return M
            if M.shape == (2, 3):
                H = np.eye(3, dtype=float)
                H[:2, :] = M
                return H
            if M.shape == (2, 2):
                A = M
                t = np.zeros(2, dtype=float)
                if translation is not None:
                    t = np.asarray(translation, dtype=float).reshape(2)
                H = np.eye(3, dtype=float)
                H[:2, :2] = A
                H[:2, 2] = t
                return H
            raise ValueError(
                "Unsupported matrix shape; expected 3x3, 2x3, or 2x2")
        else:
            t = np.asarray(translation, dtype=float).reshape(2)
            H = np.eye(3, dtype=float)
            H[:2, 2] = t
            return H

    @staticmethod
    def _apply(T: np.ndarray, points: np.ndarray) -> list[list[float]]:
        if T.shape != (3, 3):
            raise ValueError("T must be 3x3 homogeneous matrix")
        n = points.shape[0]
        ones = np.ones((n, 1), dtype=float)
        homog = np.hstack([points.astype(float), ones])
        out = homog @ T.T
        out = out[:, :2]
        return out.tolist()

    @staticmethod
    def _rotation_matrix(angle: float, degrees: bool = True) -> np.ndarray:
        theta = math.radians(angle) if degrees else angle
        c = math.cos(theta)
        s = math.sin(theta)
        R = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=float)
        return R

    @staticmethod
    def _translation_matrix(tx: float, ty: float) -> np.ndarray:
        T = np.eye(3, dtype=float)
        T[0, 2] = tx
        T[1, 2] = ty
        return T

    @staticmethod
    def _scale_matrix(sx: float, sy: float) -> np.ndarray:
        S = np.array([[sx, 0.0, 0.0], [0.0, sy, 0.0],
                     [0.0, 0.0, 1.0]], dtype=float)
        return S

    @staticmethod
    def _shear_matrix(shx: float = 0.0, shy: float = 0.0, degrees: bool = False) -> np.ndarray:
        if degrees:
            shx = math.tan(math.radians(shx))
            shy = math.tan(math.radians(shy))
        Sh = np.array([[1.0, shx, 0.0], [shy, 1.0, 0.0],
                      [0.0, 0.0, 1.0]], dtype=float)
        return Sh

    def _compose_from_operations(self, ops: Iterable[dict]) -> np.ndarray:
        T_total = np.eye(3, dtype=float)
        for op in ops:
            if not isinstance(op, dict) or "type" not in op:
                raise ValueError(
                    "Each transform must be a dict with a 'type' key")
            typ = str(op["type"]).lower()

            if typ in ("translate", "translation", "t"):
                tx = float(op.get("tx", op.get("x", op.get("dx", 0.0))))
                ty = float(op.get("ty", op.get("y", op.get("dy", 0.0))))
                T = self._translation_matrix(tx, ty)

            elif typ in ("rotate", "rotation", "r"):
                angle = float(op.get("angle", op.get("theta", 0.0)))
                degrees = bool(op.get("degrees", True))
                cx, cy = 0.0, 0.0
                if "center" in op:
                    c = op["center"]
                    cx, cy = float(c[0]), float(c[1])
                elif "cx" in op or "cy" in op:
                    cx = float(op.get("cx", 0.0))
                    cy = float(op.get("cy", 0.0))
                T = (
                    self._translation_matrix(cx, cy)
                    @ self._rotation_matrix(angle, degrees=degrees)
                    @ self._translation_matrix(-cx, -cy)
                )

            elif typ in ("scale", "s"):
                if "s" in op:
                    sx = sy = float(op["s"])
                else:
                    sx = float(op.get("sx", op.get("x", 1.0)))
                    sy = float(op.get("sy", op.get("y", 1.0)))
                cx, cy = 0.0, 0.0
                if "center" in op:
                    c = op["center"]
                    cx, cy = float(c[0]), float(c[1])
                elif "cx" in op or "cy" in op:
                    cx = float(op.get("cx", 0.0))
                    cy = float(op.get("cy", 0.0))
                T = (
                    self._translation_matrix(cx, cy)
                    @ self._scale_matrix(sx, sy)
                    @ self._translation_matrix(-cx, -cy)
                )

            elif typ in ("shear", "sh"):
                degrees = bool(op.get("degrees", False))
                shx = float(op.get("shx", op.get("x", 0.0)))
                shy = float(op.get("shy", op.get("y", 0.0)))
                cx, cy = 0.0, 0.0
                if "center" in op:
                    c = op["center"]
                    cx, cy = float(c[0]), float(c[1])
                elif "cx" in op or "cy" in op:
                    cx = float(op.get("cx", 0.0))
                    cy = float(op.get("cy", 0.0))
                T = (
                    self._translation_matrix(cx, cy)
                    @ self._shear_matrix(shx, shy, degrees=degrees)
                    @ self._translation_matrix(-cx, -cy)
                )

            elif typ in ("matrix", "affine"):
                M = op.get("matrix", op.get("affine"))
                t = op.get("translation", op.get("t"))
                T = self._to_homogeneous_matrix(M, t)

            else:
                raise ValueError(f"Unknown transform type: {typ}")

            T_total = T @ T_total

        return T_total

    @staticmethod
    def _estimate_affine(src: np.ndarray, dst: np.ndarray, tol: float = 1e-9) -> np.ndarray:
        if src.shape != dst.shape or src.ndim != 2 or src.shape[1] != 2:
            raise ValueError(
                "source_points and target_points must be Nx2 with same shape")
        n = src.shape[0]
        if n < 2:
            # With <2 points, default to identity (insufficient constraints)
            return np.eye(3, dtype=float)
        # Build design matrix for 2x3 affine: [x y 1] * [[a11 a12 a13],[a21 a22 a23]]^T = [x' y']
        X = np.hstack([src.astype(float), np.ones((n, 1), dtype=float)])  # Nx3
        Y = dst.astype(float)  # Nx2
        # Solve X @ B = Y for B (3x2), then assemble into 3x3
        B, residuals, rank, s = np.linalg.lstsq(X, Y, rcond=None)
        if rank < 2 and n >= 2:
            # Degenerate, fallback to identity
            T = np.eye(3, dtype=float)
            return T
        T = np.eye(3, dtype=float)
        T[:2, :2] = B[:2, :].T
        T[:2, 2] = B[2, :]
        return T
