import pytest
import snippet_3 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    serializable_0 = module_0.Serializable()
    assert f'{type(serializable_0).__module__}.{type(serializable_0).__qualname__}' == 'snippet_3.Serializable'
    assert f'{type(module_0.Serializable.load).__module__}.{type(module_0.Serializable.load).__qualname__}' == 'builtins.method'
    none_type_0 = None
    serializable_0.save(none_type_0)