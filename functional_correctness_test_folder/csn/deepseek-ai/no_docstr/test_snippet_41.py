import pytest
import snippet_41 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    str_0 = '.ELa!\x0cyl+5foa4^U'
    float_0 = 1461.499075
    lazy_property_0 = module_0.lazy_property(float_0)
    assert f'{type(lazy_property_0).__module__}.{type(lazy_property_0).__qualname__}' == 'snippet_41.lazy_property'
    assert lazy_property_0.fget == pytest.approx(1461.499075, abs=0.01, rel=0.01)
    var_0 = lazy_property_0.__get__(none_type_0, str_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_41.lazy_property'
    assert var_0.fget == pytest.approx(1461.499075, abs=0.01, rel=0.01)
    var_0.__get__(float_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = 1545
    bool_0 = False
    lazy_property_0 = module_0.lazy_property(bool_0)
    assert f'{type(lazy_property_0).__module__}.{type(lazy_property_0).__qualname__}' == 'snippet_41.lazy_property'
    assert lazy_property_0.fget is False
    lazy_property_0.__get__(int_0, int_0)