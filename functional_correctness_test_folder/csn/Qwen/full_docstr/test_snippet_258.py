import pytest
import snippet_258 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    r_gsolution_0 = module_0.RGsolution(none_type_0, none_type_0, none_type_0)
    assert module_0.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    r_gsolution_0.plot(none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '58mY'
    r_gsolution_0 = module_0.RGsolution(str_0, str_0, str_0)
    assert module_0.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    r_gsolution_0.plot(r_gsolution_0, scale=str_0)

def test_case_2():
    none_type_0 = None
    r_gsolution_0 = module_0.RGsolution(none_type_0, none_type_0, none_type_0)
    assert module_0.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)