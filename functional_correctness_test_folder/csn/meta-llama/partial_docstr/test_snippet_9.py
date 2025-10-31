import pytest
import snippet_9 as module_0

def test_case_0():
    int_0 = -4170
    none_type_0 = None
    record_thread_0 = module_0.RecordThread(int_0, none_type_0)
    assert f'{type(record_thread_0).__module__}.{type(record_thread_0).__qualname__}' == 'snippet_9.RecordThread'
    assert f'{type(module_0.RecordThread.id).__module__}.{type(module_0.RecordThread.id).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordThread.name).__module__}.{type(module_0.RecordThread.name).__qualname__}' == 'builtins.member_descriptor'

def test_case_1():
    int_0 = -3323
    record_thread_0 = module_0.RecordThread(int_0, int_0)
    assert f'{type(record_thread_0).__module__}.{type(record_thread_0).__qualname__}' == 'snippet_9.RecordThread'
    assert f'{type(module_0.RecordThread.id).__module__}.{type(module_0.RecordThread.id).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordThread.name).__module__}.{type(module_0.RecordThread.name).__qualname__}' == 'builtins.member_descriptor'
    var_0 = record_thread_0.__repr__()
    assert var_0 == '(id=-3323, name=-3323)'

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b'.u\x1ep=\x1b\x96\x8d'
    none_type_0 = None
    record_thread_0 = module_0.RecordThread(none_type_0, bytes_0)
    assert f'{type(record_thread_0).__module__}.{type(record_thread_0).__qualname__}' == 'snippet_9.RecordThread'
    assert f'{type(module_0.RecordThread.id).__module__}.{type(module_0.RecordThread.id).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordThread.name).__module__}.{type(module_0.RecordThread.name).__qualname__}' == 'builtins.member_descriptor'
    record_thread_0.__format__(bytes_0)