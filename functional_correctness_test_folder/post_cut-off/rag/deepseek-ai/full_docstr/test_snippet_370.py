import pytest
import snippet_370 as module_0

def test_case_0():
    module_0.SimpleRegistryClient()

@pytest.mark.xfail(strict=True)
def test_case_1():
    module_0.SimpleRegistryClient()
    str_0 = '@Y1g2$T_\t3?_8D#'
    simple_registry_client_0 = module_0.SimpleRegistryClient(str_0)
    simple_registry_client_0.search_servers(str_0)