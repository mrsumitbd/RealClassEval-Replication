class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        self.tol = 1e-8

    def _strip_leading_zeros(self, coeffs):
        # coeffs in descending powers
        i = 0
        n = len(coeffs)
        while i < n - 1 and abs(coeffs[i]) <= self.tol:
            i += 1
        return coeffs[i:]

    def _ensure_descending(self, coeffs, order=None):
        # Accept ascending or descending. Default assume descending.
        if order is None:
            return list(coeffs)
        order = str(order).lower()
        if order in ('asc', 'ascending', 'low_to_high', 'low2high', 'const_first'):
            return list(reversed(coeffs))
        return list(coeffs)

    def _eval_poly(self, coeffs_desc, x):
        # Horner's method
        v = 0.0
        for c in coeffs_desc:
            v = v * x + c
        return v

    def _parse_equation(self, equation):
        # Returns coefficients in descending order
        s = equation.strip().replace(' ', '')
        # Normalize equality if present
        if '=' in s:
            left, right = s.split('=', 1)
            # Move right to left: left - right
            s = f'({left})-({right})'

        # Determine variable symbol
        var = None
        for ch in s:
            if ch.isalpha():
                var = ch
                break
        # If no variable, treat as constant polynomial
        if var is None:
            try:
                constant = float(s)
            except Exception:
                # If cannot parse, return zero polynomial
                constant = 0.0
            return [constant]

        # Replace '-' with '+-' to split on '+'
        s = s.replace('-', '+-')
        # Remove redundant leading '+'
        if s.startswith('+-'):
            pass
        elif s.startswith('+'):
            s = s[1:]

        # Split into terms
        terms = [t for t in s.split('+') if t]

        # For exponent markers, accept '^' or '**'
        # We'll parse manually
        from collections import defaultdict
        coef_by_deg = defaultdict(float)

        for term in terms:
            # Remove surrounding parentheses if any
            while term.startswith('(') and term.endswith(')') and len(term) >= 2:
                term = term[1:-1]

            # Skip empty
            if not term:
                continue

            if var in term:
                # Normalize multiplications out
                t = term.replace('*', '')
                # Find position of var
                idx = t.find(var)
                coef_str = t[:idx]
                rest = t[idx + 1:]  # after var

                # Coefficient parsing
                if coef_str in ('', '+'):
                    coef = 1.0
                elif coef_str == '-':
                    coef = -1.0
                else:
                    try:
                        coef = float(coef_str)
                    except Exception:
                        # If malformed like '2(' etc. ignore term
                        continue

                # Exponent parsing
                deg = 1
                if rest:
                    if rest.startswith('**'):
                        expo_str = rest[2:]
                    elif rest.startswith('^'):
                        expo_str = rest[1:]
                    else:
                        expo_str = None
                    if expo_str is not None and expo_str != '':
                        # Strip possible parentheses
                        if expo_str.startswith('(') and expo_str.endswith(')'):
                            expo_str = expo_str[1:-1]
                        try:
                            deg = int(float(expo_str))
                        except Exception:
                            # If failed, default to 1
                            deg = 1
                coef_by_deg[deg] += coef
            else:
                # Constant term
                try:
                    coef = float(term)
                except Exception:
                    continue
                coef_by_deg[0] += coef

        if not coef_by_deg:
            return [0.0]

        max_deg = max(coef_by_deg.keys())
        coeffs_desc = [0.0] * (max_deg + 1)
        for d, c in coef_by_deg.items():
            coeffs_desc[max_deg - d] = c
        # Strip leading zeros
        coeffs_desc = self._strip_leading_zeros(coeffs_desc)
        return coeffs_desc

    def _real_clean_roots(self, roots, interval=None, tol=None):
        if tol is None:
            tol = self.tol
        real_roots = []
        for r in roots:
            if isinstance(r, complex):
                if abs(r.imag) <= 1e3 * tol:
                    v = r.real
                else:
                    continue
            else:
                v = float(r)
            # Snap near-integers
            nv = round(v)
            if abs(v - nv) <= 1e2 * tol:
                v = float(nv)
            real_roots.append(float(v))

        # Filter by interval if provided
        if interval is not None and len(interval) == 2:
            a, b = float(interval[0]), float(interval[1])
            lo, hi = (a, b) if a <= b else (b, a)
            real_roots = [x for x in real_roots if (
                lo - 1e2 * tol) <= x <= (hi + 1e2 * tol)]

        # Deduplicate close roots (cluster)
        real_roots.sort()
        dedup = []
        for v in real_roots:
            if not dedup:
                dedup.append(v)
            else:
                if abs(v - dedup[-1]) <= max(1e-7, 1e2 * tol):
                    # Average to reduce noise
                    dedup[-1] = 0.5 * (dedup[-1] + v)
                else:
                    dedup.append(v)
        return dedup

    def _roots_from_coeffs(self, coeffs_desc):
        coeffs_desc = self._strip_leading_zeros(list(coeffs_desc))
        # Handle zero polynomial or constant
        if not coeffs_desc:
            return []
        if len(coeffs_desc) == 1:
            # c = 0 has infinite roots; otherwise none
            if abs(coeffs_desc[0]) <= self.tol:
                return []
            return []
        # Degree
        deg = len(coeffs_desc) - 1

        # Try numpy for general case
        try:
            import numpy as np
            roots = np.roots(np.array(coeffs_desc, dtype=np.complex128))
            return [complex(r) for r in roots]
        except Exception:
            # Fallback for deg 1 and 2
            import cmath
            a = coeffs_desc[0]
            if deg == 1:
                b = coeffs_desc[1]
                if abs(a) <= self.tol:
                    return []
                return [complex(-b / a)]
            if deg == 2:
                b, c = coeffs_desc[1], coeffs_desc[2]
                if abs(a) <= self.tol:
                    if abs(b) <= self.tol:
                        return []
                    return [complex(-c / b)]
                disc = b * b - 4.0 * a * c
                sqrt_disc = cmath.sqrt(disc)
                return [(-b + sqrt_disc) / (2.0 * a), (-b - sqrt_disc) / (2.0 * a)]
            # Higher-degree without numpy: cannot solve
            return []

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise ValueError('Problem must be a dictionary')

        tol = float(problem.get('tolerance', self.tol))

        coeffs_desc = None
        if 'coefficients' in problem:
            coeffs = problem['coefficients']
            order = problem.get('order')
            coeffs_desc = self._ensure_descending(coeffs, order=order)
        elif 'equation' in problem:
            coeffs_desc = self._parse_equation(problem['equation'])
        else:
            raise ValueError(
                'Problem must contain "coefficients" or "equation"')

        roots_c = self._roots_from_coeffs(coeffs_desc)
        interval = problem.get('interval') or problem.get('range')
        real_roots = self._real_clean_roots(
            roots_c, interval=interval, tol=tol)

        return real_roots

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

        # Extract solution roots
        if isinstance(solution, dict):
            if 'roots' in solution:
                sol_roots = solution['roots']
            elif 'result' in solution:
                sol_roots = solution['result']
            else:
                return False
        else:
            sol_roots = solution

        # Ensure iterable of numbers
        try:
            roots_list = list(sol_roots)
        except Exception:
            return False

        # Determine coefficients from problem
        tol = float(problem.get('tolerance', self.tol))
        coeffs_desc = None
        if 'coefficients' in problem:
            coeffs_desc = self._ensure_descending(
                problem['coefficients'], order=problem.get('order'))
        elif 'equation' in problem:
            coeffs_desc = self._parse_equation(problem['equation'])
        else:
            return False

        if not coeffs_desc:
            # Degenerate zero polynomial or invalid; accept only empty solution
            return len(roots_list) == 0

        # Validate each supplied root: must be real and satisfy polynomial within tolerance
        for r in roots_list:
            try:
                if isinstance(r, complex):
                    if abs(r.imag) > 1e3 * tol:
                        return False
                    x = float(r.real)
                else:
                    x = float(r)
            except Exception:
                return False
            val = self._eval_poly(coeffs_desc, x)
            scale = max(1.0, sum(abs(c) for c in coeffs_desc))
            if abs(val) > 1e3 * tol * scale:
                return False

        # If expected roots provided in problem, compare sets (order-free)
        expected = None
        for key in ('expected_roots', 'roots', 'solution', 'expected'):
            if key in problem and isinstance(problem[key], (list, tuple)):
                expected = list(problem[key])
                break

        if expected is not None:
            # Clean and compare sets with tolerance, accounting for multiplicities
            def clean_list(lst):
                cleaned = []
                for v in lst:
                    if isinstance(v, complex):
                        if abs(v.imag) <= 1e3 * tol:
                            cleaned.append(float(v.real))
                        else:
                            # ignore non-real if expecting real
                            continue
                    else:
                        cleaned.append(float(v))
                cleaned.sort()
                return cleaned

            exp_clean = clean_list(expected)
            sol_clean = clean_list(roots_list)

            # Match with tolerance, multiplicity-aware
            used = [False] * len(sol_clean)
            for e in exp_clean:
                found = False
                for i, s in enumerate(sol_clean):
                    if not used[i] and abs(e - s) <= 1e3 * tol:
                        used[i] = True
                        found = True
                        break
                if not found:
                    return False
            # Ensure no extra unmatched roots if exact match required
            if len([u for u in used if u]) != len(exp_clean):
                return False

        return True
