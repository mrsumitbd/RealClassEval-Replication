import snippet_249 as module_0

def test_case_0():
    template_0 = module_0.Template()
    assert f'{type(template_0).__module__}.{type(template_0).__qualname__}' == 'snippet_249.Template'
    assert template_0.input == 'default.html'
    assert template_0.output == 'stdout'
    assert template_0.env is None