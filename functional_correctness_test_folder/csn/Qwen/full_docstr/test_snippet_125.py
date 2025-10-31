import pytest
import snippet_125 as module_0

def test_case_0():
    bool_0 = True
    fenwick_min_0 = module_0.FenwickMin(bool_0)
    assert f'{type(fenwick_min_0).__module__}.{type(fenwick_min_0).__qualname__}' == 'snippet_125.FenwickMin'
    assert f'{type(fenwick_min_0.s).__module__}.{type(fenwick_min_0.s).__qualname__}' == 'builtins.list'
    assert len(fenwick_min_0.s) == 2
    fenwick_min_0.update(bool_0, fenwick_min_0)
    bool_1 = False
    var_0 = fenwick_min_0.prefixMin(bool_1)
    assert var_0 == pytest.approx(1e309, abs=0.01, rel=0.01)

def test_case_1():
    bool_0 = True
    fenwick_min_0 = module_0.FenwickMin(bool_0)
    assert f'{type(fenwick_min_0).__module__}.{type(fenwick_min_0).__qualname__}' == 'snippet_125.FenwickMin'
    assert f'{type(fenwick_min_0.s).__module__}.{type(fenwick_min_0.s).__qualname__}' == 'builtins.list'
    assert len(fenwick_min_0.s) == 2

def test_case_2():
    bool_0 = False
    bool_1 = True
    fenwick_min_0 = module_0.FenwickMin(bool_1)
    assert f'{type(fenwick_min_0).__module__}.{type(fenwick_min_0).__qualname__}' == 'snippet_125.FenwickMin'
    assert f'{type(fenwick_min_0.s).__module__}.{type(fenwick_min_0.s).__qualname__}' == 'builtins.list'
    assert len(fenwick_min_0.s) == 2
    fenwick_min_0.update(bool_0, bool_0)

def test_case_3():
    float_0 = -2429.0
    bool_0 = True
    fenwick_min_0 = module_0.FenwickMin(bool_0)
    assert f'{type(fenwick_min_0).__module__}.{type(fenwick_min_0).__qualname__}' == 'snippet_125.FenwickMin'
    assert f'{type(fenwick_min_0.s).__module__}.{type(fenwick_min_0.s).__qualname__}' == 'builtins.list'
    assert len(fenwick_min_0.s) == 2
    var_0 = fenwick_min_0.prefixMin(float_0)
    assert var_0 == pytest.approx(1e309, abs=0.01, rel=0.01)

def test_case_4():
    bool_0 = False
    int_0 = 846
    fenwick_min_0 = module_0.FenwickMin(int_0)
    assert f'{type(fenwick_min_0).__module__}.{type(fenwick_min_0).__qualname__}' == 'snippet_125.FenwickMin'
    assert f'{type(fenwick_min_0.s).__module__}.{type(fenwick_min_0.s).__qualname__}' == 'builtins.list'
    assert len(fenwick_min_0.s) == 847
    fenwick_min_0.update(bool_0, int_0)