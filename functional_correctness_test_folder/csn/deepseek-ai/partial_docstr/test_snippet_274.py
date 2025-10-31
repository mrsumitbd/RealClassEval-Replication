import snippet_274 as module_0

def test_case_0():
    bool_0 = False
    base_permission_0 = module_0.BasePermission()
    assert f'{type(base_permission_0).__module__}.{type(base_permission_0).__qualname__}' == 'snippet_274.BasePermission'
    assert module_0.BasePermission.message is None
    var_0 = base_permission_0.has_permission(bool_0, bool_0)
    assert var_0 is True

def test_case_1():
    tuple_0 = ()
    base_permission_0 = module_0.BasePermission()
    assert f'{type(base_permission_0).__module__}.{type(base_permission_0).__qualname__}' == 'snippet_274.BasePermission'
    assert module_0.BasePermission.message is None
    var_0 = base_permission_0.has_object_permission(tuple_0, tuple_0, tuple_0)
    assert var_0 is True