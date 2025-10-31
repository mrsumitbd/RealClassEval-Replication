import pytest
import snippet_48 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    eigenvectors_complex_0 = module_0.EigenvectorsComplex()
    eigenvectors_complex_0.solve(eigenvectors_complex_0)

def test_case_1():
    eigenvectors_complex_0 = module_0.EigenvectorsComplex()
    none_type_0 = None
    eigenvectors_complex_0.is_solution(eigenvectors_complex_0, none_type_0)

def test_case_2():
    module_0.EigenvectorsComplex()