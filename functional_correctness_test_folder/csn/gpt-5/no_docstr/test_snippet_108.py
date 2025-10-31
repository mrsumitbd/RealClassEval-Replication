import pytest
import builtins as module_0
import snippet_108 as module_1

def test_case_0():
    complex_0 = -1647.70311 + 1439j
    dict_0 = {}
    object_0 = module_0.object(**dict_0)
    list_0 = [object_0, dict_0, dict_0]
    details_0 = module_1.Details(list_0)
    assert f'{type(details_0).__module__}.{type(details_0).__qualname__}' == 'snippet_108.Details'
    assert f'{type(details_0.details).__module__}.{type(details_0.details).__qualname__}' == 'builtins.list'
    assert len(details_0.details) == 3
    assert f'{type(module_1.Details.all).__module__}.{type(module_1.Details.all).__qualname__}' == 'builtins.property'
    with pytest.raises(AttributeError):
        details_0.__getattr__(complex_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = 'TsB@,\x0bFH8iP'
    details_0 = module_1.Details(str_0)
    assert f'{type(details_0).__module__}.{type(details_0).__qualname__}' == 'snippet_108.Details'
    assert details_0.details == 'TsB@,\x0bFH8iP'
    assert f'{type(module_1.Details.all).__module__}.{type(module_1.Details.all).__qualname__}' == 'builtins.property'
    details_0.__getattr__(str_0)

def test_case_2():
    bool_0 = False
    details_0 = module_1.Details(bool_0)
    assert f'{type(details_0).__module__}.{type(details_0).__qualname__}' == 'snippet_108.Details'
    assert details_0.details is False
    assert f'{type(module_1.Details.all).__module__}.{type(module_1.Details.all).__qualname__}' == 'builtins.property'