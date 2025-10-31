import pytest
import snippet_169 as module_0

def test_case_0():
    cursor_0 = module_0.Cursor()
    assert f'{type(cursor_0).__module__}.{type(cursor_0).__qualname__}' == 'snippet_169.Cursor'
    with pytest.raises(NotImplementedError):
        cursor_0.count()

def test_case_1():
    cursor_0 = module_0.Cursor()
    assert f'{type(cursor_0).__module__}.{type(cursor_0).__qualname__}' == 'snippet_169.Cursor'
    with pytest.raises(NotImplementedError):
        cursor_0.__iter__()