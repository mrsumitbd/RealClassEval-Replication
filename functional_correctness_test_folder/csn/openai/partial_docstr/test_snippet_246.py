import pytest
import apidoc.object.config as module_0
import snippet_246 as module_1

def test_case_0():
    config_0 = module_0.Config()
    assert f'{type(config_0).__module__}.{type(config_0).__qualname__}' == 'apidoc.object.config.Config'
    assert len(config_0) == 3
    config_1 = module_1.Config()
    assert f'{type(config_1).__module__}.{type(config_1).__qualname__}' == 'snippet_246.Config'
    var_0 = config_1.get_template_from_config(config_0)
    assert var_0 == '/Users/umroot/Documents/MISC_use/pynguin_folder/template/default.html'
    config_2 = module_1.Config()
    assert f'{type(config_2).__module__}.{type(config_2).__qualname__}' == 'snippet_246.Config'
    config_2.validate(config_0)

def test_case_1():
    none_type_0 = None
    config_0 = module_1.Config()
    assert f'{type(config_0).__module__}.{type(config_0).__qualname__}' == 'snippet_246.Config'
    with pytest.raises(Exception):
        config_0.validate(none_type_0)