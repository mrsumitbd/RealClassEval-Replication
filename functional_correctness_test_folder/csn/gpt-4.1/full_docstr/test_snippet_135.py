import snippet_135 as module_0

def test_case_0():
    no_op_trace_id_0 = module_0.NoOpTraceId()
    assert f'{type(no_op_trace_id_0).__module__}.{type(no_op_trace_id_0).__qualname__}' == 'snippet_135.NoOpTraceId'
    assert no_op_trace_id_0.start_time == '00000000'
    assert module_0.NoOpTraceId.VERSION == '1'
    assert module_0.NoOpTraceId.DELIMITER == '-'

def test_case_1():
    no_op_trace_id_0 = module_0.NoOpTraceId()
    assert f'{type(no_op_trace_id_0).__module__}.{type(no_op_trace_id_0).__qualname__}' == 'snippet_135.NoOpTraceId'
    assert no_op_trace_id_0.start_time == '00000000'
    assert module_0.NoOpTraceId.VERSION == '1'
    assert module_0.NoOpTraceId.DELIMITER == '-'
    var_0 = no_op_trace_id_0.to_id()
    assert var_0 == '1-00000000-000000000000000000000000'