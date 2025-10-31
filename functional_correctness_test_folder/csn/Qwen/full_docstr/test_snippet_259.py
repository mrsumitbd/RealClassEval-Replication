import pytest
import snippet_259 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    w_cxf_0 = module_0.WCxf()
    assert f'{type(w_cxf_0).__module__}.{type(w_cxf_0).__qualname__}' == 'snippet_259.WCxf'
    assert f'{type(module_0.WCxf.load).__module__}.{type(module_0.WCxf.load).__qualname__}' == 'builtins.method'
    w_cxf_0.dump()

def test_case_1():
    str_0 = 'x_P'
    w_cxf_0 = module_0.WCxf()
    assert f'{type(w_cxf_0).__module__}.{type(w_cxf_0).__qualname__}' == 'snippet_259.WCxf'
    assert f'{type(module_0.WCxf.load).__module__}.{type(module_0.WCxf.load).__qualname__}' == 'builtins.method'
    with pytest.raises(ValueError):
        w_cxf_0.dump(fmt=str_0)