import snippet_48 as module_0
import datetime as module_1

def test_case_0():
    datetime_0 = module_0.Datetime()
    assert f'{type(datetime_0).__module__}.{type(datetime_0).__qualname__}' == 'snippet_48.Datetime'
    datetime_1 = datetime_0.now()
    assert f'{type(datetime_1).__module__}.{type(datetime_1).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_1.datetime.hour).__module__}.{type(module_1.datetime.hour).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.minute).__module__}.{type(module_1.datetime.minute).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.second).__module__}.{type(module_1.datetime.second).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.microsecond).__module__}.{type(module_1.datetime.microsecond).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.tzinfo).__module__}.{type(module_1.datetime.tzinfo).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.fold).__module__}.{type(module_1.datetime.fold).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.min).__module__}.{type(module_1.datetime.min).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_1.datetime.max).__module__}.{type(module_1.datetime.max).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_1.datetime.resolution).__module__}.{type(module_1.datetime.resolution).__qualname__}' == 'datetime.timedelta'
    bytes_0 = datetime_0.pack(datetime_1)
    assert module_1.MINYEAR == 1
    assert module_1.MAXYEAR == 9999
    assert f'{type(module_1.datetime_CAPI).__module__}.{type(module_1.datetime_CAPI).__qualname__}' == 'builtins.PyCapsule'
    datetime_2 = datetime_0.unpack(bytes_0)
    assert f'{type(datetime_2).__module__}.{type(datetime_2).__qualname__}' == 'datetime.datetime'

def test_case_1():
    datetime_0 = module_0.Datetime()
    assert f'{type(datetime_0).__module__}.{type(datetime_0).__qualname__}' == 'snippet_48.Datetime'
    datetime_1 = datetime_0.now()
    assert f'{type(datetime_1).__module__}.{type(datetime_1).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_1.datetime.hour).__module__}.{type(module_1.datetime.hour).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.minute).__module__}.{type(module_1.datetime.minute).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.second).__module__}.{type(module_1.datetime.second).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.microsecond).__module__}.{type(module_1.datetime.microsecond).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.tzinfo).__module__}.{type(module_1.datetime.tzinfo).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.fold).__module__}.{type(module_1.datetime.fold).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.datetime.min).__module__}.{type(module_1.datetime.min).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_1.datetime.max).__module__}.{type(module_1.datetime.max).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_1.datetime.resolution).__module__}.{type(module_1.datetime.resolution).__qualname__}' == 'datetime.timedelta'