import pytest
import snippet_257 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\x7f(\xad\xe7ZA\xa4\xb3\x94X&1u\x9c\xcfk(Q\x01'
    user_profile_service_0 = module_0.UserProfileService()
    assert f'{type(user_profile_service_0).__module__}.{type(user_profile_service_0).__qualname__}' == 'snippet_257.UserProfileService'
    user_profile_service_0.lookup(bytes_0)

def test_case_1():
    bool_0 = True
    list_0 = [bool_0, bool_0, bool_0, bool_0]
    user_profile_service_0 = module_0.UserProfileService()
    assert f'{type(user_profile_service_0).__module__}.{type(user_profile_service_0).__qualname__}' == 'snippet_257.UserProfileService'
    user_profile_service_0.save(list_0)