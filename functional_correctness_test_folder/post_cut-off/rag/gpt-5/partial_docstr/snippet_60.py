import numpy as np
from typing import Any, Dict, Iterable, List, Tuple, Union

Number = Union[int, float]


class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        self.default_tolerance = 1e-8

    def _extract_coefficients(self, problem: Dict[str, Any]) -> np.ndarray:
        coefs = (
            problem.get('coefficients')
            or problem.get('coefs')
            or problem.get('poly')
            or problem.get('polynomial')
        )
        if coefs is None:
            raise ValueError(
                "Problem must include 'coefficients' (or 'coefs'/'poly'/'polynomial').")
        coefs = np.asarray(list(coefs), dtype=float)

        if coefs.ndim != 1 or coefs.size == 0:
            raise ValueError(
                "Coefficients must be a non-empty 1D list or array.")

        ascending = bool(problem.get('ascending', False))
        if ascending:
            coefs = coefs[::-1]

        # Trim leading zeros (highest degree first). Keep at least one coeff.
        nz = np.flatnonzero(np.abs(coefs) > 0)
        if nz.size == 0:
            # Identically zero polynomial; keep a single zero coefficient to represent 0.
            return np.array([0.0])
        first = nz[0]
        return coefs[first:]

    def _poly_value(self, coefs: np.ndarray, x: float) -> float:
        # Horner's method; coefs are in descending powers.
        y = 0.0
        for c in coefs:
            y = y * x + c
        return y

    def _cluster_sorted(self, values: Iterable[float], tol: float) -> List[float]:
        vals = sorted(float(v) for v in values)
        if not vals:
            return []
        clustered = [vals[0]]
        for v in vals[1:]:
            if abs(v - clustered[-1]) <= tol:
                # Merge by averaging for stability
                clustered[-1] = (clustered[-1] + v) / 2.0
            else:
                clustered.append(v)
        return clustered

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        tol = float(problem.get('tolerance', self.default_tolerance))
        # Optional decimal places for rounding
        precision = problem.get('precision', None)
        interval = problem.get('interval', None)    # Optional (a, b)

        coefs = self._extract_coefficients(problem)

        # Handle constant polynomials explicitly
        if coefs.size == 1:
            c0 = coefs[0]
            if abs(c0) <= tol:
                # Identically zero polynomial: every real number is a root.
                # Return empty set to indicate no finite representation.
                return {'roots': []}
            else:
                return {'roots': []}

        # Degree 1 (linear): ax + b = 0
        if coefs.size == 2:
            a, b = coefs
            if abs(a) <= tol:
                # Degenerate to constant
                roots = [] if abs(b) > tol else []
            else:
                roots = [-b / a]
        else:
            # General polynomial: use numpy.roots
            r = np.roots(coefs)
            # Select real roots by small imaginary part
            real_mask = np.isfinite(r) & (np.abs(r.imag) <= max(tol, 1e-12))
            roots = r.real[real_mask].tolist()

        # Filter by interval if provided
        if interval is not None:
            a, b = interval
            lo, hi = (min(a, b), max(a, b))
            roots = [x for x in roots if (lo - tol) <= x <= (hi + tol)]

        # Deduplicate close roots
        merge_tol = max(tol, 1e-9)
        roots = self._cluster_sorted(roots, merge_tol)

        # Optional rounding to given precision
        if isinstance(precision, int) and precision >= 0:
            roots = [round(x, precision) for x in roots]

        return {'roots': roots}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        tol = float(problem.get('tolerance', self.default_tolerance))
        interval = problem.get('interval', None)

        # Normalize solution input to list of floats
        if solution is None:
            return False
        if isinstance(solution, dict):
            roots = solution.get('roots')
        else:
            roots = solution
        if roots is None:
            return False
        try:
            roots_list = [float(x) for x in roots]
        except Exception:
            return False

        coefs = self._extract_coefficients(problem)

        # Identically zero polynomial: accept any provided roots as valid
        if coefs.size == 1 and abs(coefs[0]) <= tol:
            return True

        # Interval constraint check
        if interval is not None:
            a, b = interval
            lo, hi = (min(a, b), max(a, b))
            for x in roots_list:
                if not (lo - tol <= x <= hi + tol):
                    return False

        # Each proposed root should approximately zero the polynomial
        for x in roots_list:
            val = self._poly_value(coefs, x)
            if not np.isfinite(val):
                return False
            if abs(val) > max(tol, 1e-8) * (1.0 + max(1.0, abs(x))):
                return False

        # Compare against solver's own computed roots for completeness
        expected = self.solve(problem).get('roots', [])
        # Cluster both lists for stability then compare lengths and pairwise closeness
        cluster_tol = max(tol, 1e-7)
        exp_c = self._cluster_sorted(expected, cluster_tol)
        sol_c = self._cluster_sorted(roots_list, cluster_tol)

        if len(exp_c) != len(sol_c):
            return False

        # Sort and compare elementwise
        exp_c_sorted = sorted(exp_c)
        sol_c_sorted = sorted(sol_c)
        for a, b in zip(exp_c_sorted, sol_c_sorted):
            if abs(a - b) > max(cluster_tol, 1e-7) * (1.0 + max(abs(a), abs(b))):
                return False

        return True
