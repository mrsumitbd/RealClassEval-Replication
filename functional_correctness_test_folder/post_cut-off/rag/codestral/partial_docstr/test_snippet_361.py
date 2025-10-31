import pytest
import snippet_361 as module_0

def test_case_0():
    o_c_i_utils_0 = module_0.OCIUtils()
    assert f'{type(o_c_i_utils_0).__module__}.{type(o_c_i_utils_0).__qualname__}' == 'snippet_361.OCIUtils'
    bool_0 = o_c_i_utils_0.is_pydantic_class(o_c_i_utils_0)
    assert bool_0 is False

@pytest.mark.xfail(strict=True)
def test_case_1():
    o_c_i_utils_0 = module_0.OCIUtils()
    assert f'{type(o_c_i_utils_0).__module__}.{type(o_c_i_utils_0).__qualname__}' == 'snippet_361.OCIUtils'
    o_c_i_utils_0.remove_signature_from_tool_description(o_c_i_utils_0, o_c_i_utils_0)