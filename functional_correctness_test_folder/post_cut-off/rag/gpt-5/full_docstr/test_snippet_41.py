import snippet_41 as module_0

def test_case_0():
    header_manager_0 = module_0.HeaderManager()
    assert f'{type(header_manager_0).__module__}.{type(header_manager_0).__qualname__}' == 'snippet_41.HeaderManager'
    assert header_manager_0.separator_char == '='
    assert header_manager_0.separator_length == 60
    assert module_0.HeaderManager.DEFAULT_SEPARATOR_CHAR == '='
    assert module_0.HeaderManager.DEFAULT_SEPARATOR_LENGTH == 60
    assert module_0.HeaderManager.DEFAULT_SPARKLES == '✦ ✧ ✦ ✧'

def test_case_1():
    header_manager_0 = module_0.HeaderManager()
    assert f'{type(header_manager_0).__module__}.{type(header_manager_0).__qualname__}' == 'snippet_41.HeaderManager'
    assert header_manager_0.separator_char == '='
    assert header_manager_0.separator_length == 60
    assert module_0.HeaderManager.DEFAULT_SEPARATOR_CHAR == '='
    assert module_0.HeaderManager.DEFAULT_SEPARATOR_LENGTH == 60
    assert module_0.HeaderManager.DEFAULT_SPARKLES == '✦ ✧ ✦ ✧'
    header_manager_0.create_header()