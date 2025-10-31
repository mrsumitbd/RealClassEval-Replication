import snippet_288 as module_0

def test_case_0():
    aspect_0 = module_0.Aspect()
    assert f'{type(aspect_0).__module__}.{type(aspect_0).__qualname__}' == 'snippet_288.Aspect'
    var_0 = aspect_0.clone()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_288.Aspect'
    var_0.getId()