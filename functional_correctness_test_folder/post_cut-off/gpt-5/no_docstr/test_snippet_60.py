import pytest
import snippet_60 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    polynomial_real_0 = module_0.PolynomialReal()
    polynomial_real_0.solve(polynomial_real_0)

def test_case_1():
    polynomial_real_0 = module_0.PolynomialReal()
    polynomial_real_0.is_solution(polynomial_real_0, polynomial_real_0)

def test_case_2():
    module_0.PolynomialReal()