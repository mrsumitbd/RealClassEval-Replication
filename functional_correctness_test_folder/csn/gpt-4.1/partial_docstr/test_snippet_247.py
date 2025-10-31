import pytest
import snippet_247 as module_0

def test_case_0():
    merger_0 = module_0.Merger()
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    merger_0.merge_extends(merger_0, merger_0, inherit=merger_0)
    with pytest.raises(TypeError):
        merger_0.merge_configs(merger_0, merger_0)

def test_case_1():
    merger_0 = module_0.Merger()
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    with pytest.raises(TypeError):
        merger_0.merge_configs(merger_0, merger_0)

def test_case_2():
    str_0 = 'IjoW;RkE|i+v>h)f0'
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    merger_0.merge_extends(str_0, str_0, inherit=list_0)
    tuple_0 = ()
    with pytest.raises(ValueError):
        merger_0.merge_sources(tuple_0)

def test_case_3():
    bytes_0 = b'~y\x99\xff\x96\xed\xfb\xf9\x97\x18{\xaf\xd8^\xab\x84~\x89e'
    merger_0 = module_0.Merger()
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    with pytest.raises(ValueError):
        merger_0.merge_sources(bytes_0)

def test_case_4():
    none_type_0 = None
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    with pytest.raises(ValueError):
        merger_0.merge_extends(list_0, none_type_0)

def test_case_5():
    float_0 = -3327.6
    dict_0 = {float_0: float_0, float_0: float_0, float_0: float_0, float_0: float_0}
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    var_0 = merger_0.merge_sources(dict_0)
    assert var_0 == pytest.approx(-3327.6, abs=0.01, rel=0.01)

def test_case_6():
    float_0 = -3347.675860156157
    dict_0 = {float_0: float_0, float_0: float_0, float_0: float_0, float_0: float_0}
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    merger_0.merge_configs(dict_0, list_0)

def test_case_7():
    bool_0 = True
    bool_1 = True
    dict_0 = {bool_1: bool_1}
    list_0 = [bool_0, bool_0, bool_0, dict_0]
    list_1 = []
    merger_0 = module_0.Merger(*list_1)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    merger_0.merge_extends(list_0, list_0, inherit=bool_0)

def test_case_8():
    float_0 = -3327.6
    dict_0 = {float_0: float_0, float_0: float_0, float_0: float_0, float_0: float_0}
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    with pytest.raises(ValueError):
        merger_0.merge_extends(dict_0, list_0, list_0)

def test_case_9():
    float_0 = -3327.6
    dict_0 = {float_0: float_0, float_0: float_0, float_0: float_0, float_0: float_0}
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    none_type_0 = None
    merger_0.merge_extends(dict_0, dict_0, float_0, none_type_0)
    with pytest.raises(ValueError):
        merger_0.merge_sources(list_0)

def test_case_10():
    float_0 = -3327.6
    dict_0 = {float_0: float_0, float_0: float_0, float_0: float_0, float_0: float_0}
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    none_type_0 = None
    merger_0.merge_extends(none_type_0, none_type_0)
    with pytest.raises(TypeError):
        merger_0.merge_configs(dict_0, dict_0)

def test_case_11():
    float_0 = -3327.6
    dict_0 = {float_0: float_0, float_0: float_0, float_0: float_0, float_0: float_0}
    list_0 = []
    merger_0 = module_0.Merger(*list_0)
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    none_type_0 = None
    with pytest.raises(ValueError):
        merger_0.merge_extends(dict_0, none_type_0, inherit=dict_0)

def test_case_12():
    none_type_0 = None
    merger_0 = module_0.Merger()
    assert f'{type(merger_0).__module__}.{type(merger_0).__qualname__}' == 'snippet_247.Merger'
    var_0 = merger_0.merge_extends(none_type_0, none_type_0)
    dict_0 = {var_0: var_0, var_0: var_0, var_0: var_0, var_0: var_0}
    list_0 = []
    merger_1 = module_0.Merger(*list_0)
    assert f'{type(merger_1).__module__}.{type(merger_1).__qualname__}' == 'snippet_247.Merger'
    merger_1.merge_configs(dict_0, list_0)
    merger_2 = module_0.Merger(*list_0)
    assert f'{type(merger_2).__module__}.{type(merger_2).__qualname__}' == 'snippet_247.Merger'
    with pytest.raises(ValueError):
        merger_2.merge_sources(dict_0)