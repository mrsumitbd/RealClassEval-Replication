import pytest
import snippet_88 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    cache_0 = module_0.Cache()
    assert f'{type(cache_0).__module__}.{type(cache_0).__qualname__}' == 'snippet_88.Cache'
    assert f'{type(module_0.config).__module__}.{type(module_0.config).__qualname__}' == 'pypyr.config.Config'
    assert module_0.config.json_ascii is False
    assert module_0.config.json_indent == 2
    assert module_0.config.pipelines_subdir == 'pipelines'
    assert module_0.config.log_config is None
    assert module_0.config.log_date_format == '%Y-%m-%d %H:%M:%S'
    assert module_0.config.log_notify_format == '%(message)s'
    assert module_0.config.log_detail_format == '%(asctime)s %(levelname)s:%(name)s:%(funcName)s: %(message)s'
    assert module_0.config.default_backoff == 'fixed'
    assert module_0.config.default_cmd_encoding is None
    assert module_0.config.default_encoding is None
    assert module_0.config.default_loader == 'pypyr.loaders.file'
    assert module_0.config.default_group == 'steps'
    assert module_0.config.default_success_group == 'on_success'
    assert module_0.config.default_failure_group == 'on_failure'
    assert module_0.config.no_cache is False
    assert module_0.config.shortcuts == {}
    assert module_0.config.vars == {}
    cache_0.get(cache_0, cache_0)

def test_case_1():
    cache_0 = module_0.Cache()
    assert f'{type(cache_0).__module__}.{type(cache_0).__qualname__}' == 'snippet_88.Cache'
    assert f'{type(module_0.config).__module__}.{type(module_0.config).__qualname__}' == 'pypyr.config.Config'
    assert module_0.config.json_ascii is False
    assert module_0.config.json_indent == 2
    assert module_0.config.pipelines_subdir == 'pipelines'
    assert module_0.config.log_config is None
    assert module_0.config.log_date_format == '%Y-%m-%d %H:%M:%S'
    assert module_0.config.log_notify_format == '%(message)s'
    assert module_0.config.log_detail_format == '%(asctime)s %(levelname)s:%(name)s:%(funcName)s: %(message)s'
    assert module_0.config.default_backoff == 'fixed'
    assert module_0.config.default_cmd_encoding is None
    assert module_0.config.default_encoding is None
    assert module_0.config.default_loader == 'pypyr.loaders.file'
    assert module_0.config.default_group == 'steps'
    assert module_0.config.default_success_group == 'on_success'
    assert module_0.config.default_failure_group == 'on_failure'
    assert module_0.config.no_cache is False
    assert module_0.config.shortcuts == {}
    assert module_0.config.vars == {}