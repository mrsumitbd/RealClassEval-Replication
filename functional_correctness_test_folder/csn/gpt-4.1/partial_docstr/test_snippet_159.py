import snippet_159 as module_0

def test_case_0():
    str_0 = '\rTmtROD~FL"GR1IiN>M*'
    style_0 = module_0.Style(str_0)
    assert f'{type(style_0).__module__}.{type(style_0).__qualname__}' == 'snippet_159.Style'
    assert style_0.lines == ['', 'TmtROD~FL"GR1IiN>M*']
    assert style_0.comments == []
    assert f'{type(module_0.Style.text).__module__}.{type(module_0.Style.text).__qualname__}' == 'builtins.property'

def test_case_1():
    int_0 = -3249
    style_0 = module_0.Style(int_0)
    assert f'{type(style_0).__module__}.{type(style_0).__qualname__}' == 'snippet_159.Style'
    assert style_0.lines == -3249
    assert style_0.comments == []
    assert f'{type(module_0.Style.text).__module__}.{type(module_0.Style.text).__qualname__}' == 'builtins.property'