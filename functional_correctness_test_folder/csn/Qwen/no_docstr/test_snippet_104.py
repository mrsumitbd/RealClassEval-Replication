import pytest
import snippet_104 as module_0

def test_case_0():
    buffer_segment_0 = module_0.BufferSegment()
    assert f'{type(buffer_segment_0).__module__}.{type(buffer_segment_0).__qualname__}' == 'snippet_104.BufferSegment'
    assert f'{type(module_0.BufferSegment.offset).__module__}.{type(module_0.BufferSegment.offset).__qualname__}' == 'builtins.property'
    with pytest.raises(NotImplementedError):
        buffer_segment_0.__len__()

def test_case_1():
    buffer_segment_0 = module_0.BufferSegment()
    assert f'{type(buffer_segment_0).__module__}.{type(buffer_segment_0).__qualname__}' == 'snippet_104.BufferSegment'
    assert f'{type(module_0.BufferSegment.offset).__module__}.{type(module_0.BufferSegment.offset).__qualname__}' == 'builtins.property'
    with pytest.raises(NotImplementedError):
        buffer_segment_0.tobytes()