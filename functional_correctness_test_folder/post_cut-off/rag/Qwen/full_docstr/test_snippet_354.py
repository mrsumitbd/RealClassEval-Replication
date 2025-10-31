import snippet_354 as module_0

def test_case_0():
    event_renderer_0 = module_0.EventRenderer()
    assert f'{type(event_renderer_0).__module__}.{type(event_renderer_0).__qualname__}' == 'snippet_354.EventRenderer'
    assert event_renderer_0.pending_function_call is None
    assert module_0.TYPE_CHECKING is False