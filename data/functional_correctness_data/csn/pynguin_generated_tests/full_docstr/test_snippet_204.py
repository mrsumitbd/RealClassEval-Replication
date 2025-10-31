import pytest
import snippet_204 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    authentication_base_0 = module_0.AuthenticationBase()
    assert f'{type(authentication_base_0).__module__}.{type(authentication_base_0).__qualname__}' == 'snippet_204.AuthenticationBase'
    authentication_base_0.authenticate_request()

def test_case_1():
    authentication_base_0 = module_0.AuthenticationBase()
    assert f'{type(authentication_base_0).__module__}.{type(authentication_base_0).__qualname__}' == 'snippet_204.AuthenticationBase'
    with pytest.raises(NotImplementedError):
        authentication_base_0.get_request_credentials()