import snippet_342 as module_0

def test_case_0():
    bool_0 = False
    maximize_0 = module_0.Maximize(bool_0)
    assert f'{type(maximize_0).__module__}.{type(maximize_0).__qualname__}' == 'snippet_342.Maximize'
    assert maximize_0.guess is False
    var_0 = maximize_0.__repr__()
    assert var_0 == 'Maximize(False)'