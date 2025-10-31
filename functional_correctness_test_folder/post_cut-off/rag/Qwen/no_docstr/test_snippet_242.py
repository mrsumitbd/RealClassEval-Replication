import pytest
import snippet_242 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = True
    immediate_flush_sink_0 = module_0.ImmediateFlushSink(bool_0)
    assert f'{type(immediate_flush_sink_0).__module__}.{type(immediate_flush_sink_0).__qualname__}' == 'snippet_242.ImmediateFlushSink'
    immediate_flush_sink_0.write(bool_0)

def test_case_1():
    none_type_0 = None
    immediate_flush_sink_0 = module_0.ImmediateFlushSink(none_type_0)
    assert f'{type(immediate_flush_sink_0).__module__}.{type(immediate_flush_sink_0).__qualname__}' == 'snippet_242.ImmediateFlushSink'

@pytest.mark.xfail(strict=True)
def test_case_2():
    immediate_flush_sink_0 = module_0.ImmediateFlushSink()
    assert f'{type(immediate_flush_sink_0).__module__}.{type(immediate_flush_sink_0).__qualname__}' == 'snippet_242.ImmediateFlushSink'
    immediate_flush_sink_0.write(immediate_flush_sink_0)

def test_case_3():
    immediate_flush_sink_0 = module_0.ImmediateFlushSink()
    assert f'{type(immediate_flush_sink_0).__module__}.{type(immediate_flush_sink_0).__qualname__}' == 'snippet_242.ImmediateFlushSink'
    immediate_flush_sink_0.flush()