import pytest
import snippet_205 as module_0

def test_case_0():
    bool_0 = False
    list_0 = [bool_0, bool_0]
    list_1 = []
    arg_filter_base_0 = module_0.ArgFilterBase(*list_1)
    assert f'{type(arg_filter_base_0).__module__}.{type(arg_filter_base_0).__qualname__}' == 'snippet_205.ArgFilterBase'
    with pytest.raises(NotImplementedError):
        arg_filter_base_0.maybe_set_arg_name(list_0)

def test_case_1():
    int_0 = 580
    int_1 = 168
    arg_filter_base_0 = module_0.ArgFilterBase()
    assert f'{type(arg_filter_base_0).__module__}.{type(arg_filter_base_0).__qualname__}' == 'snippet_205.ArgFilterBase'
    with pytest.raises(NotImplementedError):
        arg_filter_base_0.filter_query(int_0, int_0, int_1)