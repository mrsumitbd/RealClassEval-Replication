
class PolynomialReal:

    def __init__(self, coefficients):
        self.coefficients = coefficients

    def solve(self, problem):
        from numpy import roots
        return roots(self.coefficients)

    def is_solution(self, problem, solution):
        value = sum(coef * (solution ** idx)
                    for idx, coef in enumerate(reversed(self.coefficients)))
        return abs(value) < 1e-6
