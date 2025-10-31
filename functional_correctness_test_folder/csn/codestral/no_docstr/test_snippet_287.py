import snippet_287 as module_0

def test_case_0():
    str_0 = 'Q\x0cYWQ!`(5\x0cL\r@ p)J\x0b'
    str_1 = 'kv-]}mC2'
    bool_0 = False
    role_0 = module_0.Role(title=str_1, can_manage=bool_0)
    assert f'{type(role_0).__module__}.{type(role_0).__qualname__}' == 'snippet_287.Role'
    assert role_0.name == ''
    assert role_0.title == 'kv-]}mC2'
    assert role_0.description == ''
    assert role_0.can_manage_roles == []
    assert role_0.is_owner is False
    assert role_0.can_manage is False
    assert role_0.can_curate is False
    assert role_0.can_view is False
    assert module_0.Role.name == ''
    assert module_0.Role.title == ''
    assert module_0.Role.description == ''
    assert module_0.Role.is_owner is False
    assert module_0.Role.can_manage is False
    assert module_0.Role.can_curate is False
    assert module_0.Role.can_view is False
    var_0 = role_0.can_manage_role(str_0)
    assert var_0 is False

def test_case_1():
    int_0 = -2592
    role_0 = module_0.Role(description=int_0)
    assert f'{type(role_0).__module__}.{type(role_0).__qualname__}' == 'snippet_287.Role'
    assert role_0.name == ''
    assert role_0.title == ''
    assert role_0.description == -2592
    assert role_0.can_manage_roles == []
    assert role_0.is_owner is False
    assert role_0.can_manage is False
    assert role_0.can_curate is False
    assert role_0.can_view is False
    assert module_0.Role.name == ''
    assert module_0.Role.title == ''
    assert module_0.Role.description == ''
    assert module_0.Role.is_owner is False
    assert module_0.Role.can_manage is False
    assert module_0.Role.can_curate is False
    assert module_0.Role.can_view is False
    var_0 = role_0.__hash__()
    assert var_0 == 0