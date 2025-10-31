import pytest
import snippet_103 as module_0

def test_case_0():
    none_type_0 = None
    reader_0 = module_0.Reader(none_type_0)
    assert f'{type(reader_0).__module__}.{type(reader_0).__qualname__}' == 'snippet_103.Reader'
    assert reader_0.s is None

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    int_0 = 177
    reader_0 = module_0.Reader(int_0)
    assert f'{type(reader_0).__module__}.{type(reader_0).__qualname__}' == 'snippet_103.Reader'
    assert reader_0.s == 177
    reader_0.readfmt(none_type_0)