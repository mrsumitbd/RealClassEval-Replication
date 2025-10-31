import pytest
import _hashlib as module_0
import snippet_183 as module_1
import suds.plugin as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    unsupported_digestmod_error_0 = module_0.UnsupportedDigestmodError()
    assert f'{type(unsupported_digestmod_error_0).__module__}.{type(unsupported_digestmod_error_0).__qualname__}' == '_hashlib.UnsupportedDigestmodError'
    assert f'{type(module_0.openssl_md_meth_names).__module__}.{type(module_0.openssl_md_meth_names).__qualname__}' == 'builtins.frozenset'
    assert len(module_0.openssl_md_meth_names) == 19
    module_1.Reader(unsupported_digestmod_error_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    plugin_container_0 = module_2.PluginContainer(none_type_0)
    assert f'{type(plugin_container_0).__module__}.{type(plugin_container_0).__qualname__}' == 'suds.plugin.PluginContainer'
    assert plugin_container_0.plugins is None
    assert f'{type(module_2.log).__module__}.{type(module_2.log).__qualname__}' == 'logging.Logger'
    assert module_2.log.filters == []
    assert module_2.log.name == 'suds.plugin'
    assert module_2.log.level == 0
    assert f'{type(module_2.log.parent).__module__}.{type(module_2.log.parent).__qualname__}' == 'logging.RootLogger'
    assert module_2.log.propagate is True
    assert module_2.log.handlers == []
    assert module_2.log.disabled is False
    assert f'{type(module_2.log.manager).__module__}.{type(module_2.log.manager).__qualname__}' == 'logging.Manager'
    assert f'{type(module_2.PluginContainer.domains).__module__}.{type(module_2.PluginContainer.domains).__qualname__}' == 'builtins.dict'
    assert len(module_2.PluginContainer.domains) == 3
    reader_0 = module_1.Reader(plugin_container_0)
    assert f'{type(reader_0).__module__}.{type(reader_0).__qualname__}' == 'snippet_183.Reader'
    assert f'{type(reader_0.options).__module__}.{type(reader_0.options).__qualname__}' == 'suds.plugin.PluginContainer'
    assert f'{type(reader_0.plugins).__module__}.{type(reader_0.plugins).__qualname__}' == 'suds.plugin.PluginContainer'
    reader_0.mangle(plugin_container_0, none_type_0)