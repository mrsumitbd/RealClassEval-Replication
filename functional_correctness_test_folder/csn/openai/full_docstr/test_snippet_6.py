import pytest
import snippet_6 as module_0

def test_case_0():
    int_0 = -4170
    none_type_0 = None
    record_file_0 = module_0.RecordFile(int_0, none_type_0)
    assert f'{type(record_file_0).__module__}.{type(record_file_0).__qualname__}' == 'snippet_6.RecordFile'
    assert f'{type(module_0.RecordFile.name).__module__}.{type(module_0.RecordFile.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordFile.path).__module__}.{type(module_0.RecordFile.path).__qualname__}' == 'builtins.member_descriptor'

def test_case_1():
    int_0 = -3323
    record_file_0 = module_0.RecordFile(int_0, int_0)
    assert f'{type(record_file_0).__module__}.{type(record_file_0).__qualname__}' == 'snippet_6.RecordFile'
    assert f'{type(module_0.RecordFile.name).__module__}.{type(module_0.RecordFile.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordFile.path).__module__}.{type(module_0.RecordFile.path).__qualname__}' == 'builtins.member_descriptor'
    var_0 = record_file_0.__repr__()
    assert var_0 == '(name=-3323, path=-3323)'

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b'.u\x1ep=\x1b\x96\x8d'
    none_type_0 = None
    record_file_0 = module_0.RecordFile(none_type_0, bytes_0)
    assert f'{type(record_file_0).__module__}.{type(record_file_0).__qualname__}' == 'snippet_6.RecordFile'
    assert f'{type(module_0.RecordFile.name).__module__}.{type(module_0.RecordFile.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordFile.path).__module__}.{type(module_0.RecordFile.path).__qualname__}' == 'builtins.member_descriptor'
    record_file_0.__format__(bytes_0)