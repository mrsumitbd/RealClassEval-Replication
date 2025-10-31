import pytest
import snippet_231 as module_0

def test_case_0():
    none_type_0 = None
    word_array_0 = module_0.WordArray(none_type_0)
    assert f'{type(word_array_0).__module__}.{type(word_array_0).__qualname__}' == 'snippet_231.WordArray'

def test_case_1():
    bytes_0 = b')\xfd \x15lRg>\xf5\x1eq\x8d\xe5>`\xbbX'
    word_array_0 = module_0.WordArray(bytes_0)
    assert f'{type(word_array_0).__module__}.{type(word_array_0).__qualname__}' == 'snippet_231.WordArray'
    var_0 = word_array_0.__len__()
    assert var_0 == pytest.approx(8.5, abs=0.01, rel=0.01)