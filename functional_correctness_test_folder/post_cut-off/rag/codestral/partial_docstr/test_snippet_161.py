import pytest
import snippet_161 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    bazi_manager_0 = module_0.BaziManager()
    assert f'{type(bazi_manager_0).__module__}.{type(bazi_manager_0).__qualname__}' == 'snippet_161.BaziManager'
    bazi_manager_0.init_tools(none_type_0, none_type_0, none_type_0, none_type_0)