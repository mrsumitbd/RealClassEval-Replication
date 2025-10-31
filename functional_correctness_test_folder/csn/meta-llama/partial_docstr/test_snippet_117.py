import pytest
import snippet_117 as module_0
import numpy.dtypes as module_1

def test_case_0():
    none_type_0 = None
    module_0.PDE(none_type_0, none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    float16_d_type_0 = module_1.Float16DType()
    p_d_e_0 = module_0.PDE(float16_d_type_0, float16_d_type_0, float16_d_type_0)
    p_d_e_0.solve()