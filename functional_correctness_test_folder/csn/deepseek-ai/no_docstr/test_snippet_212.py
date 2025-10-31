import pytest
import snippet_212 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    three_nine_utils_0 = module_0.ThreeNineUtils()
    assert f'{type(three_nine_utils_0).__module__}.{type(three_nine_utils_0).__qualname__}' == 'snippet_212.ThreeNineUtils'
    three_nine_utils_0.get_39label(three_nine_utils_0)

def test_case_1():
    three_nine_utils_0 = module_0.ThreeNineUtils()
    assert f'{type(three_nine_utils_0).__module__}.{type(three_nine_utils_0).__qualname__}' == 'snippet_212.ThreeNineUtils'
    int_0 = 2059
    dict_0 = three_nine_utils_0.get_39days(int_0)
    assert f'{type(dict_0).__module__}.{type(dict_0).__qualname__}' == 'collections.OrderedDict'
    assert len(dict_0) == 12