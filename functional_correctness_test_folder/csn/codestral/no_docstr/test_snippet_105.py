import pytest
import snippet_105 as module_0

def test_case_0():
    buffer_with_segments_collection_0 = module_0.BufferWithSegmentsCollection()
    assert f'{type(buffer_with_segments_collection_0).__module__}.{type(buffer_with_segments_collection_0).__qualname__}' == 'snippet_105.BufferWithSegmentsCollection'
    with pytest.raises(NotImplementedError):
        buffer_with_segments_collection_0.__len__()

def test_case_1():
    none_type_0 = None
    buffer_with_segments_collection_0 = module_0.BufferWithSegmentsCollection()
    assert f'{type(buffer_with_segments_collection_0).__module__}.{type(buffer_with_segments_collection_0).__qualname__}' == 'snippet_105.BufferWithSegmentsCollection'
    with pytest.raises(NotImplementedError):
        buffer_with_segments_collection_0.__getitem__(none_type_0)