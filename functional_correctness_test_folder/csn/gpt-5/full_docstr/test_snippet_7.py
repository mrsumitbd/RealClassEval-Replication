import pytest
import snippet_7 as module_0

def test_case_0():
    none_type_0 = None
    record_level_0 = module_0.RecordLevel(none_type_0, none_type_0, none_type_0)
    assert f'{type(record_level_0).__module__}.{type(record_level_0).__qualname__}' == 'snippet_7.RecordLevel'
    assert f'{type(module_0.RecordLevel.icon).__module__}.{type(module_0.RecordLevel.icon).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordLevel.name).__module__}.{type(module_0.RecordLevel.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordLevel.no).__module__}.{type(module_0.RecordLevel.no).__qualname__}' == 'builtins.member_descriptor'

def test_case_1():
    bool_0 = False
    record_level_0 = module_0.RecordLevel(bool_0, bool_0, bool_0)
    assert f'{type(record_level_0).__module__}.{type(record_level_0).__qualname__}' == 'snippet_7.RecordLevel'
    assert f'{type(module_0.RecordLevel.icon).__module__}.{type(module_0.RecordLevel.icon).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordLevel.name).__module__}.{type(module_0.RecordLevel.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordLevel.no).__module__}.{type(module_0.RecordLevel.no).__qualname__}' == 'builtins.member_descriptor'
    var_0 = record_level_0.__repr__()
    assert var_0 == '(name=False, no=False, icon=False)'

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    record_level_0 = module_0.RecordLevel(none_type_0, none_type_0, none_type_0)
    assert f'{type(record_level_0).__module__}.{type(record_level_0).__qualname__}' == 'snippet_7.RecordLevel'
    assert f'{type(module_0.RecordLevel.icon).__module__}.{type(module_0.RecordLevel.icon).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordLevel.name).__module__}.{type(module_0.RecordLevel.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.RecordLevel.no).__module__}.{type(module_0.RecordLevel.no).__qualname__}' == 'builtins.member_descriptor'
    record_level_0.__format__(none_type_0)