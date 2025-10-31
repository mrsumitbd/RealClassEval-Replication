import snippet_17 as module_0

def test_case_0():
    none_type_0 = None
    variable_0 = module_0.Variable(none_type_0, none_type_0)
    assert f'{type(variable_0).__module__}.{type(variable_0).__qualname__}' == 'snippet_17.Variable'
    assert variable_0.val is None
    assert variable_0.type is None

def test_case_1():
    dict_0 = {}
    variable_0 = module_0.Variable(dict_0, dict_0)
    assert f'{type(variable_0).__module__}.{type(variable_0).__qualname__}' == 'snippet_17.Variable'
    assert variable_0.val == {}
    assert variable_0.type == {}
    variable_1 = module_0.Variable(variable_0, dict_0)
    assert f'{type(variable_1).__module__}.{type(variable_1).__qualname__}' == 'snippet_17.Variable'
    assert f'{type(variable_1.val).__module__}.{type(variable_1.val).__qualname__}' == 'snippet_17.Variable'
    assert variable_1.type == {}
    var_0 = variable_1.__str__()
    assert var_0 == '{}'