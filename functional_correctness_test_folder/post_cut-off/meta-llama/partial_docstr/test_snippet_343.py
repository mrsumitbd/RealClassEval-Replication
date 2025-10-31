import snippet_343 as module_0

def test_case_0():
    bool_0 = False
    minimize_0 = module_0.Minimize(bool_0)
    assert f'{type(minimize_0).__module__}.{type(minimize_0).__qualname__}' == 'snippet_343.Minimize'
    assert minimize_0.guess is False
    var_0 = minimize_0.__repr__()
    assert var_0 == 'Minimize(False)'