import pytest
import snippet_198 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    module_0.RSA_PSS_Mechanism(none_type_0, none_type_0, none_type_0, none_type_0)

def test_case_1():
    bool_0 = True
    r_s_a__p_s_s__mechanism_0 = module_0.RSA_PSS_Mechanism(bool_0, bool_0, bool_0, bool_0)
    r_s_a__p_s_s__mechanism_0.to_native()