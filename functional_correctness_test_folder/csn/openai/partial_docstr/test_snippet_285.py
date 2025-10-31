import pytest
import snippet_285 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    tuple_0 = ()
    list_0 = [tuple_0]
    r_i_o_tag_0 = module_0.RIOTag(list_0, list_0)
    assert f'{type(r_i_o_tag_0).__module__}.{type(r_i_o_tag_0).__qualname__}' == 'snippet_285.RIOTag'
    assert r_i_o_tag_0.rfile == [()]
    assert r_i_o_tag_0.name == [()]
    r_i_o_tag_0.__setitem__(none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    r_i_o_tag_0 = module_0.RIOTag(none_type_0, none_type_0)
    assert f'{type(r_i_o_tag_0).__module__}.{type(r_i_o_tag_0).__qualname__}' == 'snippet_285.RIOTag'
    assert r_i_o_tag_0.rfile is None
    assert r_i_o_tag_0.name is None
    r_i_o_tag_0.close()