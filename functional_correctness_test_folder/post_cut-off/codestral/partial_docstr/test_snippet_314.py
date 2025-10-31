import pytest
import snippet_314 as module_0
import bedrock_server_manager.error as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    discovery_mixin_0 = module_0.DiscoveryMixin()
    assert f'{type(discovery_mixin_0).__module__}.{type(discovery_mixin_0).__qualname__}' == 'snippet_314.DiscoveryMixin'
    str_0 = '[Y!CrxTp%/#*'
    discovery_mixin_0.validate_server(str_0)

def test_case_1():
    discovery_mixin_0 = module_0.DiscoveryMixin()
    assert f'{type(discovery_mixin_0).__module__}.{type(discovery_mixin_0).__qualname__}' == 'snippet_314.DiscoveryMixin'
    none_type_0 = None
    with pytest.raises(module_1.MissingArgumentError):
        discovery_mixin_0.validate_server(none_type_0)