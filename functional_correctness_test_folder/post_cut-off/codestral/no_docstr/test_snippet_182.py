import pytest
import snippet_182 as module_0

def test_case_0():
    output_sink_0 = module_0.OutputSink()
    assert f'{type(output_sink_0).__module__}.{type(output_sink_0).__qualname__}' == 'snippet_182.OutputSink'
    none_type_0 = output_sink_0.finalize()
    with pytest.raises(NotImplementedError):
        output_sink_0.write(none_type_0)

def test_case_1():
    output_sink_0 = module_0.OutputSink()
    assert f'{type(output_sink_0).__module__}.{type(output_sink_0).__qualname__}' == 'snippet_182.OutputSink'
    output_sink_0.finalize()