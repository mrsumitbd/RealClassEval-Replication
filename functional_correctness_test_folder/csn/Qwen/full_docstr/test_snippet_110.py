import pytest
import snippet_110 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    enum_0 = module_0.Enum()
    assert f'{type(enum_0).__module__}.{type(enum_0).__qualname__}' == 'snippet_110.Enum'
    assert f'{type(module_0.Enum.iteritems).__module__}.{type(module_0.Enum.iteritems).__qualname__}' == 'builtins.method'
    enum_0.__repr__()