import pytest
import snippet_153 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b"';\xdbn\xb5\xdd"
    str_0 = "?\rET\n+.T^-$0'O$T"
    module_0.SelectorPattern(bytes_0, str_0)

def test_case_1():
    str_0 = '*'
    int_0 = 1596
    str_1 = 'dPYnfOZhA]T2'
    selector_pattern_0 = module_0.SelectorPattern(str_1, str_1)
    assert f'{type(selector_pattern_0).__module__}.{type(selector_pattern_0).__qualname__}' == 'snippet_153.SelectorPattern'
    assert selector_pattern_0.name == 'dPYnfOZhA]T2'
    assert f'{type(selector_pattern_0.re_pattern).__module__}.{type(selector_pattern_0.re_pattern).__qualname__}' == 're.Pattern'
    selector_pattern_0.match(str_0, int_0, int_0)

def test_case_2():
    str_0 = '*'
    int_0 = 1596
    str_1 = 'dPYnfOZhA]T2'
    selector_pattern_0 = module_0.SelectorPattern(str_1, str_1)
    assert f'{type(selector_pattern_0).__module__}.{type(selector_pattern_0).__qualname__}' == 'snippet_153.SelectorPattern'
    assert selector_pattern_0.name == 'dPYnfOZhA]T2'
    assert f'{type(selector_pattern_0.re_pattern).__module__}.{type(selector_pattern_0.re_pattern).__qualname__}' == 're.Pattern'
    str_2 = selector_pattern_0.get_name()
    assert str_2 == 'dPYnfOZhA]T2'
    selector_pattern_0.match(str_0, int_0, int_0)