import pytest
import snippet_50 as module_0
import scipy.sparse.linalg.matfuncs as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    f_f_t_convolution_0 = module_0.FFTConvolution()
    f_f_t_convolution_0.solve(f_f_t_convolution_0)

def test_case_1():
    f_f_t_convolution_0 = module_0.FFTConvolution()
    f_f_t_convolution_0.is_solution(f_f_t_convolution_0, f_f_t_convolution_0)

def test_case_2():
    module_0.FFTConvolution()

def test_case_3():
    f_f_t_convolution_0 = module_0.FFTConvolution()
    var_0 = module_1.__dir__()
    f_f_t_convolution_0.is_solution(var_0, var_0)