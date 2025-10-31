import pytest
import snippet_56 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    f_f_t_complex_scipy_f_f_tpack_0 = module_0.FFTComplexScipyFFTpack()
    f_f_t_complex_scipy_f_f_tpack_0.solve(f_f_t_complex_scipy_f_f_tpack_0)

def test_case_1():
    f_f_t_complex_scipy_f_f_tpack_0 = module_0.FFTComplexScipyFFTpack()
    f_f_t_complex_scipy_f_f_tpack_0.is_solution(f_f_t_complex_scipy_f_f_tpack_0, f_f_t_complex_scipy_f_f_tpack_0)

def test_case_2():
    module_0.FFTComplexScipyFFTpack()

@pytest.mark.xfail(strict=True)
def test_case_3():
    f_f_t_complex_scipy_f_f_tpack_0 = module_0.FFTComplexScipyFFTpack()
    f_f_t_complex_scipy_f_f_tpack_1 = module_0.FFTComplexScipyFFTpack()
    none_type_0 = None
    var_0 = f_f_t_complex_scipy_f_f_tpack_0.is_solution(none_type_0, f_f_t_complex_scipy_f_f_tpack_0)
    var_1 = var_0.__neg__()
    f_f_t_complex_scipy_f_f_tpack_0.is_solution(var_1, var_0)
    f_f_t_complex_scipy_f_f_tpack_1.solve(f_f_t_complex_scipy_f_f_tpack_1)