import pytest
import snippet_74 as module_0

def test_case_0():
    none_type_0 = None
    plain_name_0 = module_0.PlainName()
    assert f'{type(plain_name_0).__module__}.{type(plain_name_0).__qualname__}' == 'snippet_74.PlainName'
    assert plain_name_0.multi_metamodel_support is True
    plain_name_0.__call__(none_type_0, none_type_0, none_type_0)

def test_case_1():
    plain_name_0 = module_0.PlainName()
    assert f'{type(plain_name_0).__module__}.{type(plain_name_0).__qualname__}' == 'snippet_74.PlainName'
    assert plain_name_0.multi_metamodel_support is True
    with pytest.raises(AssertionError):
        plain_name_0.__call__(plain_name_0, plain_name_0, plain_name_0)

def test_case_2():
    plain_name_0 = module_0.PlainName()
    assert f'{type(plain_name_0).__module__}.{type(plain_name_0).__qualname__}' == 'snippet_74.PlainName'
    assert plain_name_0.multi_metamodel_support is True