import pytest
import snippet_98 as module_0

def test_case_0():
    bool_0 = True
    l_c_model_0 = module_0.LCModel()
    assert f'{type(l_c_model_0).__module__}.{type(l_c_model_0).__qualname__}' == 'snippet_98.LCModel'
    with pytest.raises(NotImplementedError):
        l_c_model_0.fit(bool_0, bool_0)

def test_case_1():
    str_0 = ''
    l_c_model_0 = module_0.LCModel()
    assert f'{type(l_c_model_0).__module__}.{type(l_c_model_0).__qualname__}' == 'snippet_98.LCModel'
    with pytest.raises(NotImplementedError):
        l_c_model_0.predict_unseen(str_0, str_0)

def test_case_2():
    int_0 = -1679
    l_c_model_0 = module_0.LCModel()
    assert f'{type(l_c_model_0).__module__}.{type(l_c_model_0).__qualname__}' == 'snippet_98.LCModel'
    l_c_model_0.extend_partial(int_0, int_0, int_0)