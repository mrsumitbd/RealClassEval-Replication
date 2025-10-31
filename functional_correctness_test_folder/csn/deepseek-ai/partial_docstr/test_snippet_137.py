import pytest
import snippet_137 as module_0

def test_case_0():
    reservoir_0 = module_0.Reservoir()
    assert f'{type(reservoir_0).__module__}.{type(reservoir_0).__qualname__}' == 'snippet_137.Reservoir'
    assert reservoir_0.traces_per_sec == 0
    assert reservoir_0.used_this_sec == 0
    assert reservoir_0.this_sec == 1758853539
    var_0 = reservoir_0.take()
    assert var_0 is False

def test_case_1():
    float_0 = 292.575
    reservoir_0 = module_0.Reservoir(float_0)
    assert f'{type(reservoir_0).__module__}.{type(reservoir_0).__qualname__}' == 'snippet_137.Reservoir'
    assert reservoir_0.traces_per_sec == pytest.approx(292.575, abs=0.01, rel=0.01)
    assert reservoir_0.used_this_sec == 0
    assert reservoir_0.this_sec == 1758853539
    var_0 = reservoir_0.take()
    assert var_0 is True
    assert reservoir_0.used_this_sec == 1

@pytest.mark.xfail(strict=True)
def test_case_2():
    list_0 = []
    reservoir_0 = module_0.Reservoir(list_0)
    assert f'{type(reservoir_0).__module__}.{type(reservoir_0).__qualname__}' == 'snippet_137.Reservoir'
    assert reservoir_0.traces_per_sec == []
    assert reservoir_0.used_this_sec == 0
    assert reservoir_0.this_sec == 1758853539
    reservoir_0.take()