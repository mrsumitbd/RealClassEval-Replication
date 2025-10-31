import pytest
import snippet_366 as module_0

def test_case_0():
    float_0 = -18.755
    base_config_0 = module_0.BaseConfig(float_0)
    assert f'{type(base_config_0).__module__}.{type(base_config_0).__qualname__}' == 'snippet_366.BaseConfig'
    assert base_config_0.project_root == pytest.approx(-18.755, abs=0.01, rel=0.01)
    assert base_config_0.json_output is False
    assert base_config_0.dry_run is False
    assert base_config_0.verbose is False
    assert module_0.TYPE_CHECKING is False
    assert module_0.verbose_mode is False
    assert module_0.BaseConfig.json_output is False
    assert module_0.BaseConfig.dry_run is False
    assert module_0.BaseConfig.verbose is False
    assert f'{type(module_0.BaseConfig.khive_config_dir).__module__}.{type(module_0.BaseConfig.khive_config_dir).__qualname__}' == 'builtins.property'
    base_config_0.update_from_cli_args(base_config_0)

def test_case_1():
    bytes_0 = b"\xb39\xa9\xcf\x81\x92'\x83\xaaD\x17\xb6c\x1d;\x18\xc1?\xf3*"
    base_config_0 = module_0.BaseConfig(bytes_0)
    assert f'{type(base_config_0).__module__}.{type(base_config_0).__qualname__}' == 'snippet_366.BaseConfig'
    assert base_config_0.project_root == b"\xb39\xa9\xcf\x81\x92'\x83\xaaD\x17\xb6c\x1d;\x18\xc1?\xf3*"
    assert base_config_0.json_output is False
    assert base_config_0.dry_run is False
    assert base_config_0.verbose is False
    assert module_0.TYPE_CHECKING is False
    assert module_0.verbose_mode is False
    assert module_0.BaseConfig.json_output is False
    assert module_0.BaseConfig.dry_run is False
    assert module_0.BaseConfig.verbose is False
    assert f'{type(module_0.BaseConfig.khive_config_dir).__module__}.{type(module_0.BaseConfig.khive_config_dir).__qualname__}' == 'builtins.property'
    none_type_0 = None
    base_config_0.update_from_cli_args(none_type_0)