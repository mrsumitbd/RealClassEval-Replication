import numpy as np

try:
    import sympy as sp
except Exception:
    sp = None


class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        self.tol = 1e-7
        self.cluster_tol = 1e-6

    def _close_enough(self, a: float, b: float) -> bool:
        scale = max(1.0, abs(a), abs(b))
        return abs(a - b) <= self.tol * scale

    def _dedup_sorted(self, values: list[float]) -> list[float]:
        if not values:
            return []
        values = sorted(values)
        out = [values[0]]
        for v in values[1:]:
            if not self._close_enough(v, out[-1]):
                out.append(v)
        return out

    def _normalize_coeffs(self, coeffs: list[float]) -> tuple[list[float], bool]:
        # Remove leading zeros
        if not coeffs:
            return [0.0], True
        c = list(coeffs)
        while len(c) > 1 and abs(c[0]) <= self.tol:
            c.pop(0)
        if len(c) == 1 and abs(c[0]) <= self.tol:
            return [0.0], True
        return c, False

    def _parse_polynomial(self, problem: dict) -> tuple[list[float], bool]:
        # Returns (coefficients_descending, identically_zero)
        # Accept keys: 'coefficients' (preferred), 'coefs', 'poly', 'polynomial', 'equation'
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dict")
        coeffs = None

        if 'coefficients' in problem:
            coeffs = problem['coefficients']
            ascending = bool(problem.get('ascending', False))
        elif 'coefs' in problem:
            coeffs = problem['coefs']
            ascending = bool(problem.get('ascending', False))
        elif 'polynomial' in problem or 'poly' in problem or 'equation' in problem:
            expr_val = problem.get('polynomial', problem.get(
                'poly', problem.get('equation')))
            if isinstance(expr_val, (list, tuple)):
                coeffs = list(expr_val)
                ascending = bool(problem.get('ascending', False))
            else:
                if sp is None:
                    raise ValueError(
                        "Sympy is required to parse polynomial strings or expressions")
                # Build a polynomial from string/expression
                expr = expr_val
                if isinstance(expr, str):
                    expr = expr.replace('^', '**')
                    expr = sp.sympify(expr)
                # If it's an equation equal to 0, move to one side
                if isinstance(expr, sp.Equality):
                    expr = expr.lhs - expr.rhs
                # Try to infer variable
                syms = sorted(list(expr.free_symbols), key=lambda s: s.name)
                if syms:
                    x = syms[0]
                else:
                    x = sp.symbols('x')
                poly = sp.Poly(expr, x)
                coeffs = [float(c) for c in poly.all_coeffs()]
                ascending = False
        else:
            raise ValueError("Problem dict missing polynomial data")

        # Convert to list of floats
        coeffs = [float(c) for c in coeffs]

        # If ascending, reverse to descending
        if 'ascending' in locals() and ascending:
            coeffs = list(reversed(coeffs))

        coeffs, ident_zero = self._normalize_coeffs(coeffs)
        return coeffs, ident_zero

    def _real_roots(self, coeffs: list[float]) -> list[float]:
        # Degree cases
        n = len(coeffs) - 1
        if n < 0:
            return []
        if n == 0:
            # Constant non-zero has no roots; zero case handled earlier
            return []
        # Use numpy.roots, then filter near-real roots
        roots = np.roots(np.array(coeffs, dtype=float))
        real_roots = []
        for r in roots:
            if abs(r.imag) <= self.tol * max(1.0, abs(r.real)):
                real_roots.append(float(r.real))
        # Deduplicate by clustering
        real_roots.sort()
        deduped = self._dedup_sorted(real_roots)
        return deduped

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        coeffs, ident_zero = self._parse_polynomial(problem)
        if ident_zero:
            return {'all_real': True, 'roots': []}
        # degree 0 case after normalization means constant != 0
        if len(coeffs) == 1:
            return {'roots': []}
        roots = self._real_roots(coeffs)
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
        try:
            coeffs, ident_zero = self._parse_polynomial(problem)
        except Exception:
            return False

        # Normalize solution format
        if isinstance(solution, dict):
            roots_prop = solution.get('roots', [])
            all_real_flag = bool(solution.get('all_real', False))
        elif isinstance(solution, (list, tuple)):
            roots_prop = list(solution)
            all_real_flag = False
        else:
            return False

        # Identically zero polynomial: any real number is a solution
        if ident_zero:
            # Accept either explicit all_real flag or any roots list
            return all_real_flag or isinstance(roots_prop, (list, tuple))

        # Check that proposed roots are real numbers and satisfy polynomial
        # Evaluate polynomial at x using Horner's method
        def eval_poly(cs, x):
            acc = 0.0
            for c in cs:
                acc = acc * x + c
            return acc

        # Clean proposed roots to floats and dedup
        cleaned = []
        try:
            for r in roots_prop:
                if isinstance(r, complex):
                    if abs(r.imag) > self.tol * max(1.0, abs(r.real)):
                        return False
                    r = r.real
                cleaned.append(float(r))
        except Exception:
            return False

        cleaned = self._dedup_sorted(sorted(cleaned))

        # Validate each proposed root satisfies polynomial within tolerance
        for r in cleaned:
            val = eval_poly(coeffs, r)
            if abs(val) > self.tol * max(1.0, abs(r) ** (len(coeffs) - 1)):
                return False

        # Compute expected real roots (deduped)
        try:
            expected = self._real_roots(coeffs)
        except Exception:
            return False

        # Compare sets within tolerance
        if len(expected) != len(cleaned):
            return False

        # Greedy matching
        used = [False] * len(cleaned)
        for er in expected:
            matched = False
            for i, cr in enumerate(cleaned):
                if not used[i] and self._close_enough(er, cr):
                    used[i] = True
                    matched = True
                    break
            if not matched:
                return False

        return True
