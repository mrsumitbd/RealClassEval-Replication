import pytest
import snippet_275 as module_0

def test_case_0():
    bool_0 = False
    signer_0 = module_0.Signer()
    assert f'{type(signer_0).__module__}.{type(signer_0).__qualname__}' == 'snippet_275.Signer'
    with pytest.raises(NotImplementedError):
        signer_0.sign(bool_0, bool_0)

def test_case_1():
    bool_0 = False
    signer_0 = module_0.Signer()
    assert f'{type(signer_0).__module__}.{type(signer_0).__qualname__}' == 'snippet_275.Signer'
    with pytest.raises(NotImplementedError):
        signer_0.verify(bool_0, bool_0, bool_0)