import pytest
import snippet_80 as module_0

def test_case_0():
    nice_repr_0 = module_0.NiceRepr()
    assert f'{type(nice_repr_0).__module__}.{type(nice_repr_0).__qualname__}' == 'snippet_80.NiceRepr'
    with pytest.raises(NotImplementedError):
        nice_repr_0.__nice__()

def test_case_1():
    nice_repr_0 = module_0.NiceRepr()
    assert f'{type(nice_repr_0).__module__}.{type(nice_repr_0).__qualname__}' == 'snippet_80.NiceRepr'
    nice_repr_0.__repr__()

def test_case_2():
    nice_repr_0 = module_0.NiceRepr()
    assert f'{type(nice_repr_0).__module__}.{type(nice_repr_0).__qualname__}' == 'snippet_80.NiceRepr'
    nice_repr_0.__str__()