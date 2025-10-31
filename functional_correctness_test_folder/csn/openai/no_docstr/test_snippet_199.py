import snippet_199 as module_0

def test_case_0():
    bool_0 = False
    uri_param_0 = module_0.UriParam(bool_0)
    assert f'{type(uri_param_0).__module__}.{type(uri_param_0).__qualname__}' == 'snippet_199.UriParam'
    var_0 = uri_param_0.__repr__()
    assert var_0 is False