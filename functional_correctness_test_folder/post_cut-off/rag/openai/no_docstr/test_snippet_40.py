import pytest
import snippet_40 as module_0
import datetime as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "og 4+'\t7"
    dict_0 = {str_0: str_0, str_0: str_0, str_0: str_0, str_0: str_0}
    session_calculator_0 = module_0.SessionCalculator()
    assert f'{type(session_calculator_0).__module__}.{type(session_calculator_0).__qualname__}' == 'snippet_40.SessionCalculator'
    assert f'{type(session_calculator_0.tz_handler).__module__}.{type(session_calculator_0.tz_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    session_calculator_0.calculate_time_data(dict_0, str_0)

def test_case_1():
    session_calculator_0 = module_0.SessionCalculator()
    assert f'{type(session_calculator_0).__module__}.{type(session_calculator_0).__qualname__}' == 'snippet_40.SessionCalculator'
    assert f'{type(session_calculator_0.tz_handler).__module__}.{type(session_calculator_0.tz_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'

def test_case_2():
    session_calculator_0 = module_0.SessionCalculator()
    assert f'{type(session_calculator_0).__module__}.{type(session_calculator_0).__qualname__}' == 'snippet_40.SessionCalculator'
    assert f'{type(session_calculator_0.tz_handler).__module__}.{type(session_calculator_0.tz_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    dict_0 = {session_calculator_0: session_calculator_0}
    timedelta_0 = module_1.timedelta()
    assert f'{type(timedelta_0).__module__}.{type(timedelta_0).__qualname__}' == 'datetime.timedelta'
    assert module_1.MINYEAR == 1
    assert module_1.MAXYEAR == 9999
    assert f'{type(module_1.datetime_CAPI).__module__}.{type(module_1.datetime_CAPI).__qualname__}' == 'builtins.PyCapsule'
    assert f'{type(module_1.timedelta.days).__module__}.{type(module_1.timedelta.days).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.seconds).__module__}.{type(module_1.timedelta.seconds).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.microseconds).__module__}.{type(module_1.timedelta.microseconds).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.resolution).__module__}.{type(module_1.timedelta.resolution).__qualname__}' == 'datetime.timedelta'
    assert f'{type(module_1.timedelta.min).__module__}.{type(module_1.timedelta.min).__qualname__}' == 'datetime.timedelta'
    assert f'{type(module_1.timedelta.max).__module__}.{type(module_1.timedelta.max).__qualname__}' == 'datetime.timedelta'
    session_calculator_0.calculate_time_data(dict_0, timedelta_0)

def test_case_3():
    session_calculator_0 = module_0.SessionCalculator()
    assert f'{type(session_calculator_0).__module__}.{type(session_calculator_0).__qualname__}' == 'snippet_40.SessionCalculator'
    assert f'{type(session_calculator_0.tz_handler).__module__}.{type(session_calculator_0.tz_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    dict_0 = {session_calculator_0: session_calculator_0}
    timedelta_0 = module_1.timedelta()
    assert f'{type(timedelta_0).__module__}.{type(timedelta_0).__qualname__}' == 'datetime.timedelta'
    assert module_1.MINYEAR == 1
    assert module_1.MAXYEAR == 9999
    assert f'{type(module_1.datetime_CAPI).__module__}.{type(module_1.datetime_CAPI).__qualname__}' == 'builtins.PyCapsule'
    assert f'{type(module_1.timedelta.days).__module__}.{type(module_1.timedelta.days).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.seconds).__module__}.{type(module_1.timedelta.seconds).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.microseconds).__module__}.{type(module_1.timedelta.microseconds).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.resolution).__module__}.{type(module_1.timedelta.resolution).__qualname__}' == 'datetime.timedelta'
    assert f'{type(module_1.timedelta.min).__module__}.{type(module_1.timedelta.min).__qualname__}' == 'datetime.timedelta'
    assert f'{type(module_1.timedelta.max).__module__}.{type(module_1.timedelta.max).__qualname__}' == 'datetime.timedelta'
    dict_1 = session_calculator_0.calculate_time_data(dict_0, timedelta_0)
    session_calculator_0.calculate_cost_predictions(dict_1, dict_1)

def test_case_4():
    session_calculator_0 = module_0.SessionCalculator()
    assert f'{type(session_calculator_0).__module__}.{type(session_calculator_0).__qualname__}' == 'snippet_40.SessionCalculator'
    assert f'{type(session_calculator_0.tz_handler).__module__}.{type(session_calculator_0.tz_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    str_0 = '*H1\x0cM=.8b'
    dict_0 = {str_0: session_calculator_0}
    timedelta_0 = module_1.timedelta()
    assert f'{type(timedelta_0).__module__}.{type(timedelta_0).__qualname__}' == 'datetime.timedelta'
    assert module_1.MINYEAR == 1
    assert module_1.MAXYEAR == 9999
    assert f'{type(module_1.datetime_CAPI).__module__}.{type(module_1.datetime_CAPI).__qualname__}' == 'builtins.PyCapsule'
    assert f'{type(module_1.timedelta.days).__module__}.{type(module_1.timedelta.days).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.seconds).__module__}.{type(module_1.timedelta.seconds).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.microseconds).__module__}.{type(module_1.timedelta.microseconds).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.timedelta.resolution).__module__}.{type(module_1.timedelta.resolution).__qualname__}' == 'datetime.timedelta'
    assert f'{type(module_1.timedelta.min).__module__}.{type(module_1.timedelta.min).__qualname__}' == 'datetime.timedelta'
    assert f'{type(module_1.timedelta.max).__module__}.{type(module_1.timedelta.max).__qualname__}' == 'datetime.timedelta'
    dict_1 = session_calculator_0.calculate_time_data(dict_0, timedelta_0)
    dict_2 = {}
    float_0 = -3171.962344
    session_calculator_0.calculate_cost_predictions(dict_2, dict_1, float_0)