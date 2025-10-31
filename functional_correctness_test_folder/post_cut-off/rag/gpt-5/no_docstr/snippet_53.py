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
        self.atol = 1e-8
        self.rtol = 1e-6

    # ------------------------- Public API -------------------------

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Mode 1: Estimate transform from correspondences
        if ('src_points' in problem or 'source_points' in problem) and ('dst_points' in problem or 'target_points' in problem):
            src = self._to_points(problem.get(
                'src_points', problem.get('source_points')))
            dst = self._to_points(problem.get(
                'dst_points', problem.get('target_points')))
            M = self._estimate_affine(src, dst)

            # If we have points to apply to, return transformed points
            apply_points = None
            if 'apply_to' in problem:
                apply_points = self._to_points(problem['apply_to'])
            elif 'points' in problem:
                apply_points = self._to_points(problem['points'])

            if apply_points is not None:
                transformed = self._apply_transform(M, apply_points)
                return self._from_points(transformed)
            # Otherwise return the matrix
            return {'matrix': self._from_matrix(M)}

        # Mode 2: Apply given transform to points
        M = self._parse_transform(problem)
        if M is not None:
            points_key = None
            for k in ('points', 'apply_to', 'inputs', 'x'):
                if k in problem:
                    points_key = k
                    break
            if points_key is None:
                # No points provided, return the matrix as solution
                return {'matrix': self._from_matrix(M)}
            pts = self._to_points(problem[points_key])
            transformed = self._apply_transform(M, pts)
            return self._from_points(transformed)

        # Fallback: if an explicit expected output is provided, return it
        for k in ('expected', 'expected_points', 'transformed_points', 'output', 'y'):
            if k in problem:
                return problem[k]

        # If nothing matches, return None indicating no computable solution
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
        try:
            # If explicit expected is provided in problem, compare directly
            explicit_expected = None
            for k in ('expected', 'expected_points', 'transformed_points', 'output', 'y'):
                if k in problem:
                    explicit_expected = problem[k]
                    break
            if explicit_expected is not None:
                return self._compare_any(explicit_expected, solution)

            # Determine mode and compute expected
            # Mode 1: Estimation from correspondences
            if ('src_points' in problem or 'source_points' in problem) and ('dst_points' in problem or 'target_points' in problem):
                src = self._to_points(problem.get(
                    'src_points', problem.get('source_points')))
                dst = self._to_points(problem.get(
                    'dst_points', problem.get('target_points')))
                M_expected = self._estimate_affine(src, dst)

                # If solution is a matrix, compare matrices
                maybe_M_sol = self._extract_matrix_from_solution(solution)
                if maybe_M_sol is not None:
                    return self._matrices_close(M_expected, maybe_M_sol)

                # Else if solution is points (transformed), compare transformed apply_to/points
                apply_points = None
                if 'apply_to' in problem:
                    apply_points = self._to_points(problem['apply_to'])
                elif 'points' in problem:
                    apply_points = self._to_points(problem['points'])
                if apply_points is None:
                    # No points to compare against, try verifying that provided matrix maps src->dst
                    return False
                expected_pts = self._apply_transform(M_expected, apply_points)
                sol_pts = self._extract_points_from_solution(solution)
                if sol_pts is None:
                    return False
                return self._points_close(expected_pts, sol_pts)

            # Mode 2: Apply given transform to points
            M = self._parse_transform(problem)
            if M is not None:
                points_key = None
                for k in ('points', 'apply_to', 'inputs', 'x'):
                    if k in problem:
                        points_key = k
                        break
                if points_key is None:
                    # Expecting a matrix from solution
                    maybe_M_sol = self._extract_matrix_from_solution(solution)
                    if maybe_M_sol is None:
                        return False
                    return self._matrices_close(M, maybe_M_sol)
                pts = self._to_points(problem[points_key])
                expected_pts = self._apply_transform(M, pts)
                sol_pts = self._extract_points_from_solution(solution)
                if sol_pts is None:
                    return False
                return self._points_close(expected_pts, sol_pts)

            # Nothing to validate against
            return False
        except Exception:
            return False

    # ------------------------- Helpers -------------------------

    def _to_points(self, pts: Any) -> np.ndarray:
        arr = np.asarray(pts, dtype=float)
        if arr.ndim != 2:
            raise ValueError('Points must be a 2D array-like of shape (N, 2)')
        if arr.shape[1] != 2 and arr.shape[0] == 2:
            arr = arr.T
        if arr.shape[1] != 2:
            raise ValueError('Points must have shape (N, 2)')
        return arr

    def _from_points(self, pts: np.ndarray):
        return pts.tolist()

    def _to_matrix3x3(self, M: Any) -> np.ndarray:
        arr = np.asarray(M, dtype=float)
        if arr.shape == (3, 3):
            return arr
        if arr.shape == (2, 3):
            out = np.eye(3, dtype=float)
            out[:2, :3] = arr
            return out
        if arr.shape == (2, 2):
            out = np.eye(3, dtype=float)
            out[:2, :2] = arr
            return out
        raise ValueError('Matrix must be 3x3, 2x3, or 2x2')

    def _from_matrix(self, M: np.ndarray):
        return M.tolist()

    def _estimate_affine(self, src: np.ndarray, dst: np.ndarray) -> np.ndarray:
        if src.shape != dst.shape or src.shape[1] != 2:
            raise ValueError('src_points and dst_points must both be (N, 2)')
        n = src.shape[0]
        if n < 1:
            raise ValueError('At least one correspondence required')

        X_aug = np.hstack([src, np.ones((n, 1), dtype=float)])
        B, _, _, _ = np.linalg.lstsq(X_aug, dst, rcond=None)  # shape (3, 2)
        M = np.array(
            [
                [B[0, 0], B[1, 0], B[2, 0]],
                [B[0, 1], B[1, 1], B[2, 1]],
                [0.0, 0.0, 1.0],
            ],
            dtype=float,
        )
        return M

    def _apply_transform(self, M: np.ndarray, pts: np.ndarray) -> np.ndarray:
        M = self._to_matrix3x3(M)
        ones = np.ones((pts.shape[0], 1), dtype=float)
        ph = np.hstack([pts, ones])  # (N,3) row vectors
        out_h = ph @ M.T
        return out_h[:, :2]

    def _parse_transform(self, problem: dict) -> np.ndarray | None:
        # Direct matrix descriptors
        for k in ('matrix', 'M', 'affine', 'transform'):
            if k in problem:
                try:
                    return self._to_matrix3x3(problem[k])
                except Exception:
                    pass
        # Linear + translation
        A = None
        t = None
        for k in ('A', 'linear', 'matrix2x2'):
            if k in problem:
                A = np.asarray(problem[k], dtype=float)
                break
        for k in ('t', 'translation', 'translate', 'b'):
            if k in problem:
                t = np.asarray(problem[k], dtype=float).reshape(-1)
                break
        if A is not None:
            M = np.eye(3, dtype=float)
            A = np.asarray(A, dtype=float)
            if A.shape != (2, 2):
                raise ValueError('Linear part must be 2x2')
            M[:2, :2] = A
            if t is not None:
                if t.shape[0] != 2:
                    raise ValueError('Translation must be length-2')
                M[:2, 2] = t
            return M

        # Parameterized operations
        ops_order = problem.get(
            'order', ['scale', 'shear', 'rotate', 'translate'])
        M = np.eye(3, dtype=float)

        # Build ops present
        ops = {}
        # Scale
        if 'scale' in problem or 'sx' in problem or 'sy' in problem:
            scale = problem.get('scale', None)
            sx = problem.get('sx', None)
            sy = problem.get('sy', None)
            if isinstance(scale, (int, float)):
                sx = float(scale) if sx is None else sx
                sy = float(scale) if sy is None else sy
            elif isinstance(scale, (list, tuple, np.ndarray)):
                arr = np.asarray(scale, dtype=float).reshape(-1)
                if arr.size == 1:
                    sx = float(arr[0]) if sx is None else sx
                    sy = float(arr[0]) if sy is None else sy
                elif arr.size >= 2:
                    sx = float(arr[0]) if sx is None else sx
                    sy = float(arr[1]) if sy is None else sy
            sx = 1.0 if sx is None else float(sx)
            sy = 1.0 if sy is None else float(sy)
            ops['scale'] = self._scale_matrix(sx, sy, center=problem.get(
                'scale_center') or problem.get('center'))

        # Shear
        if 'shear' in problem or 'shx' in problem or 'shy' in problem or 'shear_degrees' in problem or 'shear_radians' in problem:
            shx = problem.get('shx', 0.0)
            shy = problem.get('shy', 0.0)
            shear = problem.get('shear', None)
            if shear is not None:
                if isinstance(shear, (int, float)):
                    shx = float(shear)
                    shy = 0.0
                else:
                    arr = np.asarray(shear, dtype=float).reshape(-1)
                    if arr.size >= 1:
                        shx = float(arr[0])
                    if arr.size >= 2:
                        shy = float(arr[1])
            if 'shear_degrees' in problem:
                val = float(problem['shear_degrees'])
                shx = math.tan(math.radians(val))
            if 'shear_radians' in problem:
                val = float(problem['shear_radians'])
                shx = math.tan(val)
            ops['shear'] = self._shear_matrix(shx, shy, center=problem.get(
                'shear_center') or problem.get('center'))

        # Rotation
        if 'rotation' in problem or 'rotate' in problem or 'angle' in problem or 'theta' in problem or 'rotation_degrees' in problem or 'rotation_radians' in problem:
            angle = None
            degrees = None
            if 'rotation' in problem:
                r = problem['rotation']
                if isinstance(r, dict):
                    if 'degrees' in r:
                        angle = float(r['degrees'])
                        degrees = True
                    elif 'radians' in r:
                        angle = float(r['radians'])
                        degrees = False
                    elif 'angle' in r:
                        angle = float(r['angle'])
                else:
                    angle = float(r)
            if 'rotate' in problem and angle is None:
                angle = float(problem['rotate'])
            if 'angle' in problem and angle is None:
                angle = float(problem['angle'])
            if 'theta' in problem and angle is None:
                angle = float(problem['theta'])
            if 'rotation_degrees' in problem:
                angle = float(problem['rotation_degrees'])
                degrees = True
            if 'rotation_radians' in problem:
                angle = float(problem['rotation_radians'])
                degrees = False
            if angle is None:
                angle = 0.0
            if degrees is None:
                degrees = bool(problem.get('degrees', True))
            ops['rotate'] = self._rotation_matrix(angle, degrees=degrees, center=problem.get(
                'rotation_center') or problem.get('center'))

        # Translation
        if 'translation' in problem or 'translate' in problem or 'tx' in problem or 'ty' in problem:
            t = problem.get('translation', problem.get('translate'))
            tx = problem.get('tx', 0.0)
            ty = problem.get('ty', 0.0)
            if t is not None:
                arr = np.asarray(t, dtype=float).reshape(-1)
                if arr.size >= 1:
                    tx = float(arr[0])
                if arr.size >= 2:
                    ty = float(arr[1])
            ops['translate'] = self._translation_matrix(tx, ty)

        if not ops:
            return None

        # Compose in order
        for name in ops_order:
            opM = ops.get(name)
            if opM is not None:
                M = opM @ M

        return M

    def _translation_matrix(self, tx: float, ty: float) -> np.ndarray:
        M = np.eye(3, dtype=float)
        M[0, 2] = tx
        M[1, 2] = ty
        return M

    def _scale_matrix(self, sx: float, sy: float, center=None) -> np.ndarray:
        S = np.eye(3, dtype=float)
        S[0, 0] = sx
        S[1, 1] = sy
        if center is None:
            return S
        cx, cy = np.asarray(center, dtype=float).reshape(-1)[:2]
        return self._translation_matrix(cx, cy) @ S @ self._translation_matrix(-cx, -cy)

    def _shear_matrix(self, shx: float, shy: float, center=None) -> np.ndarray:
        Sh = np.eye(3, dtype=float)
        Sh[0, 1] = float(shx)
        Sh[1, 0] = float(shy)
        if center is None:
            return Sh
        cx, cy = np.asarray(center, dtype=float).reshape(-1)[:2]
        return self._translation_matrix(cx, cy) @ Sh @ self._translation_matrix(-cx, -cy)

    def _rotation_matrix(self, angle: float, degrees: bool = True, center=None) -> np.ndarray:
        theta = math.radians(angle) if degrees else float(angle)
        c = math.cos(theta)
        s = math.sin(theta)
        R = np.eye(3, dtype=float)
        R[0, 0] = c
        R[0, 1] = -s
        R[1, 0] = s
        R[1, 1] = c
        if center is None:
            return R
        cx, cy = np.asarray(center, dtype=float).reshape(-1)[:2]
        return self._translation_matrix(cx, cy) @ R @ self._translation_matrix(-cx, -cy)

    def _extract_matrix_from_solution(self, sol: Any) -> np.ndarray | None:
        if isinstance(sol, dict):
            for k in ('matrix', 'M', 'affine', 'transform'):
                if k in sol:
                    try:
                        return self._to_matrix3x3(sol[k])
                    except Exception:
                        return None
        # If solution is directly a matrix-like
        try:
            arr = np.asarray(sol, dtype=float)
            if arr.shape in ((3, 3), (2, 3), (2, 2)):
                return self._to_matrix3x3(arr)
        except Exception:
            pass
        return None

    def _extract_points_from_solution(self, sol: Any) -> np.ndarray | None:
        if isinstance(sol, dict):
            for k in ('transformed_points', 'points', 'output', 'y', 'result'):
                if k in sol:
                    try:
                        return self._to_points(sol[k])
                    except Exception:
                        return None
        try:
            arr = self._to_points(sol)
            return arr
        except Exception:
            return None

    def _points_close(self, a: np.ndarray, b: np.ndarray) -> bool:
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        if a.shape != b.shape:
            return False
        return np.allclose(a, b, rtol=self.rtol, atol=self.atol)

    def _matrices_close(self, A: np.ndarray, B: np.ndarray) -> bool:
        A = self._to_matrix3x3(A)
        B = self._to_matrix3x3(B)
        return np.allclose(A, B, rtol=self.rtol, atol=self.atol)

    def _compare_any(self, expected: Any, got: Any) -> bool:
        # Try matrix compare
        M_exp = self._extract_matrix_from_solution(expected)
        M_got = self._extract_matrix_from_solution(got)
        if M_exp is not None and M_got is not None:
            return self._matrices_close(M_exp, M_got)

        # Try points compare
        P_exp = self._extract_points_from_solution(expected)
        P_got = self._extract_points_from_solution(got)
        if P_exp is not None and P_got is not None:
            return self._points_close(P_exp, P_got)

        # Fallback to numpy allclose if arrays; else equality
        try:
            a = np.asarray(expected, dtype=float)
            b = np.asarray(got, dtype=float)
            if a.shape == b.shape:
                return np.allclose(a, b, rtol=self.rtol, atol=self.atol)
        except Exception:
            pass
        return expected == got
