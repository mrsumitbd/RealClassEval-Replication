import pytest
import snippet_180 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'BrO7P'
    str_1 = 'mzr=X:'
    dict_0 = {str_0: str_0, str_1: str_0}
    module_0.Immutable(**dict_0)

def test_case_1():
    immutable_0 = module_0.Immutable()
    assert f'{type(immutable_0).__module__}.{type(immutable_0).__qualname__}' == 'snippet_180.Immutable'
    assert f'{type(module_0.AnyStr).__module__}.{type(module_0.AnyStr).__qualname__}' == 'typing.TypeVar'
    immutable_1 = module_0.Immutable()
    assert f'{type(immutable_1).__module__}.{type(immutable_1).__qualname__}' == 'snippet_180.Immutable'
    with pytest.raises(AttributeError):
        immutable_1.__setattr__(immutable_0, immutable_0)