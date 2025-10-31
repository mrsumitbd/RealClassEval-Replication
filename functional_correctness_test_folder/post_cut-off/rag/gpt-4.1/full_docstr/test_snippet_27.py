import pytest
import claude_monitor.utils.time_utils as module_0
import snippet_27 as module_1
import datetime as module_2

def test_case_0():
    str_0 = 'z,n@6EKGb\t269D@]{'
    timezone_handler_0 = module_0.TimezoneHandler()
    assert f'{type(timezone_handler_0).__module__}.{type(timezone_handler_0).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    assert f'{type(timezone_handler_0.default_tz).__module__}.{type(timezone_handler_0.default_tz).__qualname__}' == 'pytz.UTC'
    assert module_0.HAS_BABEL is True
    assert f'{type(module_0.logger).__module__}.{type(module_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.logger.filters == []
    assert module_0.logger.name == 'claude_monitor.utils.time_utils'
    assert module_0.logger.level == 0
    assert f'{type(module_0.logger.parent).__module__}.{type(module_0.logger.parent).__qualname__}' == 'logging.RootLogger'
    assert module_0.logger.propagate is True
    assert module_0.logger.handlers == []
    assert module_0.logger.disabled is False
    assert f'{type(module_0.logger.manager).__module__}.{type(module_0.logger.manager).__qualname__}' == 'logging.Manager'
    timestamp_processor_0 = module_1.TimestampProcessor(timezone_handler_0)
    assert f'{type(timestamp_processor_0).__module__}.{type(timestamp_processor_0).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_0.timezone_handler).__module__}.{type(timestamp_processor_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    timestamp_processor_0.parse_timestamp(str_0)

def test_case_1():
    none_type_0 = None
    none_type_1 = None
    timestamp_processor_0 = module_1.TimestampProcessor(none_type_1)
    assert f'{type(timestamp_processor_0).__module__}.{type(timestamp_processor_0).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_0.timezone_handler).__module__}.{type(timestamp_processor_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    timestamp_processor_0.parse_timestamp(none_type_0)

def test_case_2():
    timestamp_processor_0 = module_1.TimestampProcessor()
    assert f'{type(timestamp_processor_0).__module__}.{type(timestamp_processor_0).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_0.timezone_handler).__module__}.{type(timestamp_processor_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    var_0 = timestamp_processor_0.parse_timestamp(timestamp_processor_0)
    timestamp_processor_0.parse_timestamp(var_0)

def test_case_3():
    int_0 = -1108
    float_0 = 2208.0
    timestamp_processor_0 = module_1.TimestampProcessor(float_0)
    assert f'{type(timestamp_processor_0).__module__}.{type(timestamp_processor_0).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert timestamp_processor_0.timezone_handler == pytest.approx(2208.0, abs=0.01, rel=0.01)
    timestamp_processor_0.parse_timestamp(int_0)
    timestamp_processor_1 = module_1.TimestampProcessor()
    assert f'{type(timestamp_processor_1).__module__}.{type(timestamp_processor_1).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_1.timezone_handler).__module__}.{type(timestamp_processor_1.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    var_0 = timestamp_processor_1.parse_timestamp(int_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_2.datetime.hour).__module__}.{type(module_2.datetime.hour).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.minute).__module__}.{type(module_2.datetime.minute).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.second).__module__}.{type(module_2.datetime.second).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.microsecond).__module__}.{type(module_2.datetime.microsecond).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.tzinfo).__module__}.{type(module_2.datetime.tzinfo).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.fold).__module__}.{type(module_2.datetime.fold).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.min).__module__}.{type(module_2.datetime.min).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_2.datetime.max).__module__}.{type(module_2.datetime.max).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_2.datetime.resolution).__module__}.{type(module_2.datetime.resolution).__qualname__}' == 'datetime.timedelta'
    var_1 = timestamp_processor_1.parse_timestamp(var_0)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'datetime.datetime'
    assert module_2.MINYEAR == 1
    assert module_2.MAXYEAR == 9999
    assert f'{type(module_2.datetime_CAPI).__module__}.{type(module_2.datetime_CAPI).__qualname__}' == 'builtins.PyCapsule'

def test_case_4():
    float_0 = 1055.16146
    bool_0 = False
    tuple_0 = (bool_0,)
    timestamp_processor_0 = module_1.TimestampProcessor(tuple_0)
    assert f'{type(timestamp_processor_0).__module__}.{type(timestamp_processor_0).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert timestamp_processor_0.timezone_handler == (False,)
    timestamp_processor_0.parse_timestamp(float_0)

def test_case_5():
    bool_0 = True
    timestamp_processor_0 = module_1.TimestampProcessor()
    assert f'{type(timestamp_processor_0).__module__}.{type(timestamp_processor_0).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_0.timezone_handler).__module__}.{type(timestamp_processor_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    timestamp_processor_1 = module_1.TimestampProcessor(bool_0)
    assert f'{type(timestamp_processor_1).__module__}.{type(timestamp_processor_1).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert timestamp_processor_1.timezone_handler is True
    var_0 = timestamp_processor_0.parse_timestamp(bool_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_2.datetime.hour).__module__}.{type(module_2.datetime.hour).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.minute).__module__}.{type(module_2.datetime.minute).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.second).__module__}.{type(module_2.datetime.second).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.microsecond).__module__}.{type(module_2.datetime.microsecond).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.tzinfo).__module__}.{type(module_2.datetime.tzinfo).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.fold).__module__}.{type(module_2.datetime.fold).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.datetime.min).__module__}.{type(module_2.datetime.min).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_2.datetime.max).__module__}.{type(module_2.datetime.max).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_2.datetime.resolution).__module__}.{type(module_2.datetime.resolution).__qualname__}' == 'datetime.timedelta'
    var_1 = timestamp_processor_0.parse_timestamp(timestamp_processor_1)
    assert module_2.MINYEAR == 1
    assert module_2.MAXYEAR == 9999
    assert f'{type(module_2.datetime_CAPI).__module__}.{type(module_2.datetime_CAPI).__qualname__}' == 'builtins.PyCapsule'
    timestamp_processor_2 = module_1.TimestampProcessor()
    assert f'{type(timestamp_processor_2).__module__}.{type(timestamp_processor_2).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_2.timezone_handler).__module__}.{type(timestamp_processor_2.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    var_2 = timestamp_processor_2.parse_timestamp(timestamp_processor_1)
    timestamp_processor_2.parse_timestamp(var_1)
    timestamp_processor_3 = module_1.TimestampProcessor(var_2)
    assert f'{type(timestamp_processor_3).__module__}.{type(timestamp_processor_3).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_3.timezone_handler).__module__}.{type(timestamp_processor_3.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    timestamp_processor_4 = module_1.TimestampProcessor()
    assert f'{type(timestamp_processor_4).__module__}.{type(timestamp_processor_4).__qualname__}' == 'snippet_27.TimestampProcessor'
    assert f'{type(timestamp_processor_4.timezone_handler).__module__}.{type(timestamp_processor_4.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    str_0 = '/Jr|5m\x0bh-XVaP\x0b5slZ'
    timestamp_processor_4.parse_timestamp(str_0)
    str_1 = '_&HaZhx%d^,{'
    timestamp_processor_3.parse_timestamp(str_1)