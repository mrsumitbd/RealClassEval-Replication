import pytest
import snippet_303 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    read_only_resource_mixin_0 = module_0.ReadOnlyResourceMixin()
    assert f'{type(read_only_resource_mixin_0).__module__}.{type(read_only_resource_mixin_0).__qualname__}' == 'snippet_303.ReadOnlyResourceMixin'
    assert module_0.ReadOnlyResourceMixin.OPERATION_CREATE == 'create'
    assert module_0.ReadOnlyResourceMixin.OPERATION_UPDATE == 'update'
    assert module_0.ReadOnlyResourceMixin.OPERATION_DELETE == 'delete'
    read_only_resource_mixin_0.create(none_type_0, none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    read_only_resource_mixin_0 = module_0.ReadOnlyResourceMixin()
    assert f'{type(read_only_resource_mixin_0).__module__}.{type(read_only_resource_mixin_0).__qualname__}' == 'snippet_303.ReadOnlyResourceMixin'
    assert module_0.ReadOnlyResourceMixin.OPERATION_CREATE == 'create'
    assert module_0.ReadOnlyResourceMixin.OPERATION_UPDATE == 'update'
    assert module_0.ReadOnlyResourceMixin.OPERATION_DELETE == 'delete'
    list_0 = []
    read_only_resource_mixin_0.update(list_0, read_only_resource_mixin_0, list_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    complex_0 = -2601.03 + 731.8153j
    none_type_0 = None
    read_only_resource_mixin_0 = module_0.ReadOnlyResourceMixin()
    assert f'{type(read_only_resource_mixin_0).__module__}.{type(read_only_resource_mixin_0).__qualname__}' == 'snippet_303.ReadOnlyResourceMixin'
    assert module_0.ReadOnlyResourceMixin.OPERATION_CREATE == 'create'
    assert module_0.ReadOnlyResourceMixin.OPERATION_UPDATE == 'update'
    assert module_0.ReadOnlyResourceMixin.OPERATION_DELETE == 'delete'
    read_only_resource_mixin_0.delete(none_type_0, none_type_0, complex_0)