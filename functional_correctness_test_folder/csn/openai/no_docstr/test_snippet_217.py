import snippet_217 as module_0

def test_case_0():
    filtered_value_indicator_0 = module_0.FilteredValueIndicator()
    assert f'{type(filtered_value_indicator_0).__module__}.{type(filtered_value_indicator_0).__qualname__}' == 'snippet_217.FilteredValueIndicator'
    str_0 = filtered_value_indicator_0.__str__()
    assert str_0 == '[Filtered]'

def test_case_1():
    filtered_value_indicator_0 = module_0.FilteredValueIndicator()
    assert f'{type(filtered_value_indicator_0).__module__}.{type(filtered_value_indicator_0).__qualname__}' == 'snippet_217.FilteredValueIndicator'
    str_0 = filtered_value_indicator_0.__str__()
    assert str_0 == '[Filtered]'
    str_1 = filtered_value_indicator_0.__repr__()
    assert str_1 == '[Filtered]'