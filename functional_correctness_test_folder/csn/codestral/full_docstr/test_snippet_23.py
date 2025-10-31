import snippet_23 as module_0

def test_case_0():
    none_type_0 = None
    strip_content_type_middleware_0 = module_0.StripContentTypeMiddleware(none_type_0)
    assert f'{type(strip_content_type_middleware_0).__module__}.{type(strip_content_type_middleware_0).__qualname__}' == 'snippet_23.StripContentTypeMiddleware'
    assert strip_content_type_middleware_0.app is None