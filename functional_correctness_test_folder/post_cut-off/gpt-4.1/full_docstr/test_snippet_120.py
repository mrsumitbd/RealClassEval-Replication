import pytest
import snippet_120 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    nunchaku_i_p_adapter_loader_0 = module_0.NunchakuIPAdapterLoader()
    assert f'{type(module_0.NunchakuIPAdapterLoader.INPUT_TYPES).__module__}.{type(module_0.NunchakuIPAdapterLoader.INPUT_TYPES).__qualname__}' == 'builtins.method'
    assert module_0.NunchakuIPAdapterLoader.RETURN_TYPES == ('MODEL', 'IPADAPTER_PIPELINE')
    assert module_0.NunchakuIPAdapterLoader.FUNCTION == 'load'
    assert module_0.NunchakuIPAdapterLoader.CATEGORY == 'Nunchaku'
    assert module_0.NunchakuIPAdapterLoader.TITLE == 'Nunchaku IP-Adapter Loader'
    nunchaku_i_p_adapter_loader_0.load(nunchaku_i_p_adapter_loader_0)

def test_case_1():
    none_type_0 = None