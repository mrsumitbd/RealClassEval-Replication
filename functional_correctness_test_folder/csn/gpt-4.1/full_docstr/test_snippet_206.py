import pytest
import snippet_206 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    stream_code_debug_0 = module_0.StreamCodeDebug()
    assert f'{type(stream_code_debug_0).__module__}.{type(stream_code_debug_0).__qualname__}' == 'snippet_206.StreamCodeDebug'
    stream_code_debug_0.op_id(stream_code_debug_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    stream_code_debug_0 = module_0.StreamCodeDebug()
    assert f'{type(stream_code_debug_0).__module__}.{type(stream_code_debug_0).__qualname__}' == 'snippet_206.StreamCodeDebug'
    stream_code_debug_0.type_code(stream_code_debug_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    stream_code_debug_0 = module_0.StreamCodeDebug()
    assert f'{type(stream_code_debug_0).__module__}.{type(stream_code_debug_0).__qualname__}' == 'snippet_206.StreamCodeDebug'
    stream_code_debug_0.flags(stream_code_debug_0)