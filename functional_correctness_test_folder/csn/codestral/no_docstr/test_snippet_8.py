import pytest
import snippet_8 as module_0

def test_case_0():
    int_0 = -4170
    none_type_0 = None
    record_process_0 = module_0.RecordProcess(int_0, none_type_0)
    assert f'{type(record_process_0).__module__}.{type(record_process_0).__qualname__}' == 'snippet_8.RecordProcess'
    assert f'{type(module_0.RecordProcess.id).__module__}.{type(module_0.RecordProcess.id).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordProcess.name).__module__}.{type(module_0.RecordProcess.name).__qualname__}' == 'builtins.member_descriptor'

def test_case_1():
    int_0 = -3323
    record_process_0 = module_0.RecordProcess(int_0, int_0)
    assert f'{type(record_process_0).__module__}.{type(record_process_0).__qualname__}' == 'snippet_8.RecordProcess'
    assert f'{type(module_0.RecordProcess.id).__module__}.{type(module_0.RecordProcess.id).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordProcess.name).__module__}.{type(module_0.RecordProcess.name).__qualname__}' == 'builtins.member_descriptor'
    var_0 = record_process_0.__repr__()
    assert var_0 == '(id=-3323, name=-3323)'

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b'.u\x1ep=\x1b\x96\x8d'
    none_type_0 = None
    record_process_0 = module_0.RecordProcess(none_type_0, bytes_0)
    assert f'{type(record_process_0).__module__}.{type(record_process_0).__qualname__}' == 'snippet_8.RecordProcess'
    assert f'{type(module_0.RecordProcess.id).__module__}.{type(module_0.RecordProcess.id).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordProcess.name).__module__}.{type(module_0.RecordProcess.name).__qualname__}' == 'builtins.member_descriptor'
    record_process_0.__format__(bytes_0)