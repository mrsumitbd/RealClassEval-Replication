import snippet_294 as module_0

def test_case_0():
    code_manager_0 = module_0.CodeManager()
    assert f'{type(code_manager_0).__module__}.{type(code_manager_0).__qualname__}' == 'snippet_294.CodeManager'
    assert code_manager_0.codes == {}
    assert code_manager_0.default_filename == 'solution.py'
    str_0 = code_manager_0.get_raw_code()
    assert str_0 == ''
    code_manager_0.update_from_response(str_0)

def test_case_1():
    code_manager_0 = module_0.CodeManager()
    assert f'{type(code_manager_0).__module__}.{type(code_manager_0).__qualname__}' == 'snippet_294.CodeManager'
    assert code_manager_0.codes == {}
    assert code_manager_0.default_filename == 'solution.py'
    str_0 = code_manager_0.get_formatted_codes()
    assert str_0 == 'No codes available.'

def test_case_2():
    code_manager_0 = module_0.CodeManager()
    assert f'{type(code_manager_0).__module__}.{type(code_manager_0).__qualname__}' == 'snippet_294.CodeManager'
    assert code_manager_0.codes == {}
    assert code_manager_0.default_filename == 'solution.py'
    str_0 = code_manager_0.get_raw_code()
    assert str_0 == ''

def test_case_3():
    code_manager_0 = module_0.CodeManager()
    assert f'{type(code_manager_0).__module__}.{type(code_manager_0).__qualname__}' == 'snippet_294.CodeManager'
    assert code_manager_0.codes == {}
    assert code_manager_0.default_filename == 'solution.py'
    bool_0 = code_manager_0.has_code()
    assert bool_0 is False

def test_case_4():
    code_manager_0 = module_0.CodeManager()
    assert f'{type(code_manager_0).__module__}.{type(code_manager_0).__qualname__}' == 'snippet_294.CodeManager'
    assert code_manager_0.codes == {}
    assert code_manager_0.default_filename == 'solution.py'