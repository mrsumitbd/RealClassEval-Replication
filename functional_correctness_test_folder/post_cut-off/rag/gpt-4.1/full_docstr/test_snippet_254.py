import pytest
import snippet_254 as module_0

def test_case_0():
    str_0 = '@!-nM'
    time_tracker_0 = module_0.TimeTracker(str_0)
    assert f'{type(time_tracker_0).__module__}.{type(time_tracker_0).__qualname__}' == 'snippet_254.TimeTracker'
    assert time_tracker_0.history_dir == '@!-nM'
    time_tracker_0.get_last_message_time(str_0)

def test_case_1():
    str_0 = '`\\eHtj*+6,-ZUN*'
    time_tracker_0 = module_0.TimeTracker(str_0)
    assert f'{type(time_tracker_0).__module__}.{type(time_tracker_0).__qualname__}' == 'snippet_254.TimeTracker'
    assert time_tracker_0.history_dir == '`\\eHtj*+6,-ZUN*'
    str_1 = time_tracker_0.get_time_elapsed_prefix(str_0)
    assert str_1 == ''

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = ''
    time_tracker_0 = module_0.TimeTracker(str_0)
    assert f'{type(time_tracker_0).__module__}.{type(time_tracker_0).__qualname__}' == 'snippet_254.TimeTracker'
    assert time_tracker_0.history_dir == ''
    var_0 = time_tracker_0.get_last_message_time(str_0)
    str_1 = time_tracker_0.format_time_elapsed(var_0, var_0)
    assert str_1 == ''
    time_tracker_0.format_time_elapsed(str_0, time_tracker_0)

def test_case_3():
    none_type_0 = None
    time_tracker_0 = module_0.TimeTracker(none_type_0)
    assert f'{type(time_tracker_0).__module__}.{type(time_tracker_0).__qualname__}' == 'snippet_254.TimeTracker'
    assert time_tracker_0.history_dir is None