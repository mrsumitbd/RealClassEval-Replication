import pytest
import snippet_173 as module_0

def test_case_0():
    bool_0 = True
    clock_0 = module_0.Clock()
    assert f'{type(clock_0).__module__}.{type(clock_0).__qualname__}' == 'snippet_173.Clock'
    assert f'{type(module_0.Clock.now_ns).__module__}.{type(module_0.Clock.now_ns).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.Clock.now_s).__module__}.{type(module_0.Clock.now_s).__qualname__}' == 'builtins.property'
    clock_0.update(bool_0)

def test_case_1():
    float_0 = -2505.065008
    clock_0 = module_0.Clock()
    assert f'{type(clock_0).__module__}.{type(clock_0).__qualname__}' == 'snippet_173.Clock'
    assert f'{type(module_0.Clock.now_ns).__module__}.{type(module_0.Clock.now_ns).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.Clock.now_s).__module__}.{type(module_0.Clock.now_s).__qualname__}' == 'builtins.property'
    with pytest.raises(ValueError):
        clock_0.update(float_0)

def test_case_2():
    clock_0 = module_0.Clock()
    assert f'{type(clock_0).__module__}.{type(clock_0).__qualname__}' == 'snippet_173.Clock'
    assert f'{type(module_0.Clock.now_ns).__module__}.{type(module_0.Clock.now_ns).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.Clock.now_s).__module__}.{type(module_0.Clock.now_s).__qualname__}' == 'builtins.property'