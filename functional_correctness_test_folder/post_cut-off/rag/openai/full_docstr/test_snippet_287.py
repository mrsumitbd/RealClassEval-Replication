import pytest
import snippet_287 as module_0
import dataclasses as module_1

def test_case_0():
    bool_0 = False
    input_interval_0 = module_0.InputInterval(bool_0)
    assert f'{type(input_interval_0).__module__}.{type(input_interval_0).__qualname__}' == 'snippet_287.InputInterval'
    assert input_interval_0.time_window is False
    assert input_interval_0.relative_time is None
    assert module_0.InputInterval.time_window is None
    assert module_0.InputInterval.relative_time is None
    assert f'{type(module_0.InputInterval.from_dict).__module__}.{type(module_0.InputInterval.from_dict).__qualname__}' == 'builtins.method'

@pytest.mark.xfail(strict=True)
def test_case_1():
    module_0.InputInterval()

def test_case_2():
    bytes_0 = b"\xb7(\xd5\x95\x1c\x8b\xda\xaf'\t&\x1b"
    var_0 = module_1.field(default_factory=bytes_0, init=bytes_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'dataclasses.Field'
    assert f'{type(module_1.MISSING).__module__}.{type(module_1.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_1.KW_ONLY).__module__}.{type(module_1.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    assert f'{type(module_1.Field.compare).__module__}.{type(module_1.Field.compare).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.default).__module__}.{type(module_1.Field.default).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.default_factory).__module__}.{type(module_1.Field.default_factory).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.hash).__module__}.{type(module_1.Field.hash).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.init).__module__}.{type(module_1.Field.init).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.kw_only).__module__}.{type(module_1.Field.kw_only).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.metadata).__module__}.{type(module_1.Field.metadata).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.name).__module__}.{type(module_1.Field.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.repr).__module__}.{type(module_1.Field.repr).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.Field.type).__module__}.{type(module_1.Field.type).__qualname__}' == 'builtins.member_descriptor'
    input_interval_0 = module_0.InputInterval(var_0)
    assert f'{type(input_interval_0).__module__}.{type(input_interval_0).__qualname__}' == 'snippet_287.InputInterval'
    assert f'{type(input_interval_0.time_window).__module__}.{type(input_interval_0.time_window).__qualname__}' == 'dataclasses.Field'
    assert input_interval_0.relative_time is None
    assert module_0.InputInterval.time_window is None
    assert module_0.InputInterval.relative_time is None
    assert f'{type(module_0.InputInterval.from_dict).__module__}.{type(module_0.InputInterval.from_dict).__qualname__}' == 'builtins.method'
    input_interval_0.to_dict()

def test_case_3():
    bool_0 = False
    dict_0 = {bool_0: bool_0}
    input_interval_0 = module_0.InputInterval(relative_time=dict_0)
    assert f'{type(input_interval_0).__module__}.{type(input_interval_0).__qualname__}' == 'snippet_287.InputInterval'
    assert input_interval_0.time_window is None
    assert input_interval_0.relative_time == {False: False}
    assert module_0.InputInterval.time_window is None
    assert module_0.InputInterval.relative_time is None
    assert f'{type(module_0.InputInterval.from_dict).__module__}.{type(module_0.InputInterval.from_dict).__qualname__}' == 'builtins.method'
    input_interval_0.to_dict()

@pytest.mark.xfail(strict=True)
def test_case_4():
    dict_0 = {}
    bool_0 = False
    set_0 = {bool_0}
    module_0.InputInterval(set_0, dict_0)