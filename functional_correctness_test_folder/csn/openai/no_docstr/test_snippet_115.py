import snippet_115 as module_0

def test_case_0():
    bool_0 = False
    variable_0 = module_0.Variable(bool_0)
    assert f'{type(variable_0).__module__}.{type(variable_0).__qualname__}' == 'snippet_115.Variable'
    assert variable_0.name is False
    var_0 = variable_0.__repr__()
    assert var_0 is False