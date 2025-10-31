import snippet_218 as module_0

def test_case_0():
    str_0 = ';Os.pK(99\rm'
    repeat_value_indicator_0 = module_0.RepeatValueIndicator(str_0)
    assert f'{type(repeat_value_indicator_0).__module__}.{type(repeat_value_indicator_0).__qualname__}' == 'snippet_218.RepeatValueIndicator'
    assert repeat_value_indicator_0.key == ';Os.pK(99\rm'

def test_case_1():
    str_0 = '!\tbF8GB8ICrq(\r^Nh>'
    repeat_value_indicator_0 = module_0.RepeatValueIndicator(str_0)
    assert f'{type(repeat_value_indicator_0).__module__}.{type(repeat_value_indicator_0).__qualname__}' == 'snippet_218.RepeatValueIndicator'
    assert repeat_value_indicator_0.key == '!\tbF8GB8ICrq(\r^Nh>'
    str_1 = repeat_value_indicator_0.__repr__()
    assert str_1 == "<same as prior '!\\tbF8GB8ICrq(\\r^Nh>'>"