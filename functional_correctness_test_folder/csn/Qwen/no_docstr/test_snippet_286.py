import pytest
import snippet_286 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    access_enum_mixin_0 = module_0.AccessEnumMixin()
    assert f'{type(access_enum_mixin_0).__module__}.{type(access_enum_mixin_0).__qualname__}' == 'snippet_286.AccessEnumMixin'
    assert f'{type(module_0.AccessEnumMixin.validate).__module__}.{type(module_0.AccessEnumMixin.validate).__qualname__}' == 'builtins.method'
    access_enum_mixin_0.__str__()