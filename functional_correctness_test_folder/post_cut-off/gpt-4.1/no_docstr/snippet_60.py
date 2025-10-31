
import re
import math


class PolynomialReal:

    def __init__(self):
        pass

    def solve(self, problem):
        # Parse the polynomial equation
        # Example: "x^2 - 5x + 6 = 0"
        lhs, rhs = problem.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        if rhs != '0':
            # Move all terms to lhs
            lhs = f"({lhs})-({rhs})"
        # Extract coefficients for x^2, x, and constant
        # Supports forms like: x^2, -x^2, 2x^2, -2x^2, x, -x, 2x, -2x, numbers
        # Remove spaces
        lhs = lhs.replace(' ', '')
        # Find all terms
        # Pattern: ([+-]?[\d\.]*)(x(?:\^2)?)?
        pattern = re.compile(r'([+-]?[\d\.]*)(x(?:\^2)?)?')
        terms = pattern.findall(lhs)
        a = b = c = 0.0
        for coef, var in terms:
            if coef == '' and var == '':
                continue
            if var == 'x^2':
                if coef in ('', '+'):
                    a += 1.0
                elif coef == '-':
                    a -= 1.0
                else:
                    a += float(coef)
            elif var == 'x':
                if coef in ('', '+'):
                    b += 1.0
                elif coef == '-':
                    b -= 1.0
                else:
                    b += float(coef)
            elif var == '':
                if coef:
                    c += float(coef)
        # Now solve ax^2 + bx + c = 0
        if abs(a) < 1e-12:
            # Linear equation bx + c = 0
            if abs(b) < 1e-12:
                # c = 0
                if abs(c) < 1e-12:
                    return []
                else:
                    return []
            else:
                x = -c / b
                return [x]
        else:
            D = b * b - 4 * a * c
            if D < -1e-12:
                return []
            elif abs(D) < 1e-12:
                x = -b / (2 * a)
                return [x]
            else:
                sqrtD = math.sqrt(D)
                x1 = (-b + sqrtD) / (2 * a)
                x2 = (-b - sqrtD) / (2 * a)
                return sorted([x1, x2])

    def is_solution(self, problem, solution):
        # Check if all values in solution satisfy the equation
        lhs, rhs = problem.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()

        def eval_poly(expr, x):
            # Replace x with value
            expr = expr.replace('^', '**')
            expr = expr.replace('x', f'({x})')
            try:
                return eval(expr)
            except Exception:
                return None
        for x in solution:
            lval = eval_poly(lhs, x)
            rval = eval_poly(rhs, x)
            if lval is None or rval is None:
                return False
            if abs(lval - rval) > 1e-6:
                return False
        return True
