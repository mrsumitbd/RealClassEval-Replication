import snippet_186 as module_0

def test_case_0():
    tns_filter_0 = module_0.TnsFilter()
    assert f'{type(tns_filter_0).__module__}.{type(tns_filter_0).__qualname__}' == 'snippet_186.TnsFilter'
    assert tns_filter_0.tns == []

def test_case_1():
    bool_0 = False
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    tns_filter_0 = module_0.TnsFilter()
    assert f'{type(tns_filter_0).__module__}.{type(tns_filter_0).__qualname__}' == 'snippet_186.TnsFilter'
    assert tns_filter_0.tns == []
    var_0 = tns_filter_0.match(dict_0, tns_filter_0)
    assert var_0 is True

def test_case_2():
    list_0 = []
    tns_filter_0 = module_0.TnsFilter(*list_0)
    assert f'{type(tns_filter_0).__module__}.{type(tns_filter_0).__qualname__}' == 'snippet_186.TnsFilter'
    assert tns_filter_0.tns == []
    bool_0 = False
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    none_type_0 = None
    var_0 = tns_filter_0.match(dict_0, none_type_0)
    assert var_0 is False