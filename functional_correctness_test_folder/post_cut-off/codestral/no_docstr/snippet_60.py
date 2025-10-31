
class PolynomialReal:

    def __init__(self):
        pass

    def solve(self, problem):
        from sympy import symbols, Eq, solve
        x = symbols('x')
        equation = Eq(problem, 0)
        solutions = solve(equation, x)
        return solutions

    def is_solution(self, problem, solution):
        from sympy import symbols, Eq
        x = symbols('x')
        equation = Eq(problem, 0)
        return equation.subs(x, solution)
