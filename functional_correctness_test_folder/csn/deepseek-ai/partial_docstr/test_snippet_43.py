import pytest
import snippet_43 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    complex_0 = 753.92 - 394.304j
    int_0 = 3548
    dict_0 = {int_0: int_0}
    tuple_0 = (int_0, int_0, dict_0, int_0)
    list_0 = [tuple_0, dict_0, dict_0]
    bool_0 = False
    response_0 = module_0.Response(list_0, bool_0)
    assert f'{type(response_0).__module__}.{type(response_0).__qualname__}' == 'snippet_43.Response'
    response_0.send(complex_0, complex_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    set_0 = set()
    response_0 = module_0.Response(set_0, set_0)
    assert f'{type(response_0).__module__}.{type(response_0).__qualname__}' == 'snippet_43.Response'
    response_0.send(set_0)

def test_case_2():
    none_type_0 = None
    int_0 = -1846
    response_0 = module_0.Response(none_type_0, int_0)
    assert f'{type(response_0).__module__}.{type(response_0).__qualname__}' == 'snippet_43.Response'