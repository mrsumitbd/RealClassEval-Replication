import pytest
import snippet_57 as module_0

def test_case_0():
    surv_0 = module_0.Surv()
    with pytest.raises(ValueError):
        surv_0.from_arrays(surv_0, surv_0, surv_0, surv_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    surv_0 = module_0.Surv()
    none_type_0 = None
    surv_0.from_arrays(none_type_0, surv_0, name_time=none_type_0)

def test_case_2():
    surv_0 = module_0.Surv()
    with pytest.raises(TypeError):
        surv_0.from_dataframe(surv_0, surv_0, surv_0)

def test_case_3():
    none_type_0 = None