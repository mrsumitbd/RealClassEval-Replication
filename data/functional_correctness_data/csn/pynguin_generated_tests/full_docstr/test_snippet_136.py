import snippet_136 as module_0

def test_case_0():
    trace_id_0 = module_0.TraceId()
    assert f'{type(trace_id_0).__module__}.{type(trace_id_0).__qualname__}' == 'snippet_136.TraceId'
    assert trace_id_0.start_time == 1758853534
    assert module_0.TraceId.VERSION == '1'
    assert module_0.TraceId.DELIMITER == '-'

def test_case_1():
    trace_id_0 = module_0.TraceId()
    assert f'{type(trace_id_0).__module__}.{type(trace_id_0).__qualname__}' == 'snippet_136.TraceId'
    assert trace_id_0.start_time == 1758853534
    assert module_0.TraceId.VERSION == '1'
    assert module_0.TraceId.DELIMITER == '-'
    trace_id_0.to_id()