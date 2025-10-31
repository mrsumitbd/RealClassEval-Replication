import pytest
import snippet_149 as module_0

def test_case_0():
    float_0 = 3353.4
    tor_config_type_0 = module_0.TorConfigType()
    assert f'{type(tor_config_type_0).__module__}.{type(tor_config_type_0).__qualname__}' == 'snippet_149.TorConfigType'
    var_0 = tor_config_type_0.parse(float_0)
    assert var_0 == pytest.approx(3353.4, abs=0.01, rel=0.01)

def test_case_1():
    tor_config_type_0 = module_0.TorConfigType()
    assert f'{type(tor_config_type_0).__module__}.{type(tor_config_type_0).__qualname__}' == 'snippet_149.TorConfigType'
    var_0 = tor_config_type_0.parse(tor_config_type_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_149.TorConfigType'
    dict_0 = {tor_config_type_0: tor_config_type_0, tor_config_type_0: tor_config_type_0}
    complex_0 = 865 - 3827.936j
    var_1 = tor_config_type_0.validate(tor_config_type_0, dict_0, complex_0)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_149.TorConfigType'