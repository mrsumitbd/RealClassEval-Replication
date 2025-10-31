
from typing import Any, Dict, List, Tuple, Optional
import math

try:
    import numpy as np
except Exception as e:
    np = None


class AffineTransform2D:
    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        pass

    def _extract_points(self, problem: Dict[str, Any]) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
        possible_src_keys = ['source_points', 'src_points', 'src', 'source']
        possible_dst_keys = ['target_points', 'dst_points', 'dst', 'target']

        src = None
        dst = None
        for k in possible_src_keys:
            if k in problem:
                src = problem[k]
                break
        for k in possible_dst_keys:
            if k in problem:
                dst = problem[k]
                break
        if src is None or dst is None:
            raise ValueError("Problem must contain source and target points.")

        def normalize_points(pts):
            out = []
            for p in pts:
                if isinstance(p, dict) and 'x' in p and 'y' in p:
                    out.append((float(p['x']), float(p['y'])))
                elif isinstance(p, (list, tuple)) and len(p) >= 2:
                    out.append((float(p[0]), float(p[1])))
                else:
                    raise ValueError("Invalid point format.")
            return out

        src_norm = normalize_points(src)
        dst_norm = normalize_points(dst)

        if len(src_norm) != len(dst_norm):
            raise ValueError(
                "Source and target must have the same number of points.")
        if len(src_norm) < 3:
            raise ValueError(
                "At least 3 point pairs are required to determine an affine transform.")

        return src_norm, dst_norm

    def _solve_affine_numpy(self, src: List[Tuple[float, float]], dst: List[Tuple[float, float]]):
        n = len(src)
        A = []
        b = []
        for i in range(n):
            x, y = src[i]
            u, v = dst[i]
            A.append([x, y, 1.0, 0.0, 0.0, 0.0])
            A.append([0.0, 0.0, 0.0, x, y, 1.0])
            b.append(u)
            b.append(v)
        A = np.asarray(A, dtype=float)
        b = np.asarray(b, dtype=float)
        params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        a11, a12, tx, a21, a22, ty = params.tolist()
        M = [[a11, a12, tx],
             [a21, a22, ty],
             [0.0, 0.0, 1.0]]
        return M

    def _solve_affine_no_numpy(self, src: List[Tuple[float, float]], dst: List[Tuple[float, float]]):
        # Solve normal equations (A^T A) p = A^T b for 6 parameters
        # Build sums to form the 6x6 normal matrix and 6x1 rhs
        Sxx = Syy = Sxy = Sx = Sy = 0.0
        Su = Sv = 0.0
        Sxu = Sxv = Syu = Syv = 0.0
        n = float(len(src))
        for (x, y), (u, v) in zip(src, dst):
            Sxx += x * x
            Syy += y * y
            Sxy += x * y
            Sx += x
            Sy += y
            Su += u
            Sv += v
            Sxu += x * u
            Sxv += x * v
            Syu += y * u
            Syv += y * v

        # The normal matrix for parameters [a11, a12, tx, a21, a22, ty]
        # Block structure allows solving two 3x3 systems independently:
        # For u: [ [Sxx, Sxy, Sx], [Sxy, Syy, Sy], [Sx, Sy, n] ] * [a11, a12, tx] = [Sxu, Syu, Su]
        # For v: same LHS * [a21, a22, ty] = [Sxv, Syv, Sv]
        def solve_3x3(M, b):
            # Gaussian elimination for 3x3
            M = [list(row) for row in M]
            b = list(b)
            for i in range(3):
                # Pivot
                pivot = i
                maxv = abs(M[i][i])
                for r in range(i + 1, 3):
                    if abs(M[r][i]) > maxv:
                        maxv = abs(M[r][i])
                        pivot = r
                if maxv == 0.0:
                    raise ValueError(
                        "Singular system; points may be collinear.")
                if pivot != i:
                    M[i], M[pivot] = M[pivot], M[i]
                    b[i], b[pivot] = b[pivot], b[i]
                # Eliminate
                for r in range(i + 1, 3):
                    if M[r][i] == 0.0:
                        continue
                    factor = M[r][i] / M[i][i]
                    for c in range(i, 3):
                        M[r][c] -= factor * M[i][c]
                    b[r] -= factor * b[i]
            # Back substitution
            x = [0.0, 0.0, 0.0]
            for i in reversed(range(3)):
                s = b[i]
                for c in range(i + 1, 3):
                    s -= M[i][c] * x[c]
                x[i] = s / M[i][i]
            return x

        L = [[Sxx, Sxy, Sx],
             [Sxy, Syy, Sy],
             [Sx,  Sy,  n]]
        rhs_u = [Sxu, Syu, Su]
        rhs_v = [Sxv, Syv, Sv]

        a11, a12, tx = solve_3x3(L, rhs_u)
        a21, a22, ty = solve_3x3(L, rhs_v)

        M = [[a11, a12, tx],
             [a21, a22, ty],
             [0.0, 0.0, 1.0]]
        return M

    def _apply(self, M: List[List[float]], pts: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        out = []
        a11, a12, tx = M[0]
        a21, a22, ty = M[1]
        for x, y in pts:
            u = a11 * x + a12 * y + tx
            v = a21 * x + a22 * y + ty
            out.append((u, v))
        return out

    def _errors(self, pred: List[Tuple[float, float]], true: List[Tuple[float, float]]) -> Tuple[List[float], float, float]:
        errs = []
        for (u1, v1), (u2, v2) in zip(pred, true):
            du = u1 - u2
            dv = v1 - v2
            errs.append(math.hypot(du, dv))
        if errs:
            rms = math.sqrt(sum(e * e for e in errs) / len(errs))
            mx = max(errs)
        else:
            rms = 0.0
            mx = 0.0
        return errs, rms, mx

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        src, dst = self._extract_points(problem)
        if np is not None:
            M = self._solve_affine_numpy(src, dst)
        else:
            M = self._solve_affine_no_numpy(src, dst)
        pred = self._apply(M, src)
        _, rms, mx = self._errors(pred, dst)
        return {
            'matrix': M,
            'rms_error': rms,
            'max_error': mx
        }

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
            tol = float(problem.get('tolerance', 1e-6))
            M = solution.get('matrix') if isinstance(solution, dict) else None
            if M is None or not (isinstance(M, (list, tuple)) and len(M) == 3):
                return False
            if any(not (isinstance(row, (list, tuple)) and len(row) == 3) for row in M):
                return False
            # Basic validation of last row if provided fully
            if abs(M[2][0]) > 1e-9 or abs(M[2][1]) > 1e-9 or abs(M[2][2] - 1.0) > 1e-6:
                # Allow slight numeric differences but enforce affine form
                return False
            pred = self._apply(M, src)
            errs, rms, mx = self._errors(pred, dst)
            if 'rms_error' in solution:
                if not isinstance(solution['rms_error'], (int, float)):
                    return False
                if abs(solution['rms_error'] - rms) > max(tol, 1e-6):
                    return False
            if 'max_error' in solution:
                if not isinstance(solution['max_error'], (int, float)):
                    return False
                if abs(solution['max_error'] - mx) > max(tol, 1e-6):
                    return False
            return all(e <= tol for e in errs)
        except Exception:
            return False
