import pytest
import snippet_57 as module_0
import numpy.f2py.f2py2e as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    f_f_t_convolution_0 = module_0.FFTConvolution()
    f_f_t_convolution_0.solve(f_f_t_convolution_0)

def test_case_1():
    f_f_t_convolution_0 = module_0.FFTConvolution()
    none_type_0 = None
    f_f_t_convolution_0.is_solution(f_f_t_convolution_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    f_f_t_convolution_0 = module_0.FFTConvolution()
    var_0 = module_1.preparse_sysargv()
    assert module_1.f2py_version == '2.2.6'
    assert module_1.numpy_version == '2.2.6'
    assert module_1.MESON_ONLY_VER is False
    var_1 = f_f_t_convolution_0.is_solution(f_f_t_convolution_0, var_0)
    var_1.blocked_domains()