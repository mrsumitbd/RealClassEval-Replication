import pytest
import snippet_58 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    l_u_factorization_0 = module_0.LUFactorization()
    l_u_factorization_0.solve(l_u_factorization_0)

def test_case_1():
    l_u_factorization_0 = module_0.LUFactorization()
    l_u_factorization_0.is_solution(l_u_factorization_0, l_u_factorization_0)

def test_case_2():
    module_0.LUFactorization()