import snippet_264 as module_0

def test_case_0():
    str_0 = '2rKv7"m P*{h/'
    str_1 = 'Rm$tz2L0Q"]S.#Tve'
    user_0 = module_0.User(str_0, str_1)
    assert f'{type(user_0).__module__}.{type(user_0).__qualname__}' == 'snippet_264.User'
    assert user_0.id == '2rKv7"m P*{h/'
    assert user_0.name == 'Rm$tz2L0Q"]S.#Tve'
    assert user_0.roles == []
    str_2 = user_0.__repr__()
    assert str_2 == 'User(id=\'2rKv7"m P*{h/\', name=\'Rm$tz2L0Q"]S.#Tve\', roles=[])'
    complex_0 = 1861.6 + 338.778j
    user_1 = module_0.User(complex_0, complex_0, complex_0)
    assert f'{type(user_1).__module__}.{type(user_1).__qualname__}' == 'snippet_264.User'
    assert user_1.id == 1861.6 + 338.778j
    assert user_1.name == 1861.6 + 338.778j
    assert user_1.roles == 1861.6 + 338.778j

def test_case_1():
    str_0 = 't~BO 4u~j:Z\n'
    user_0 = module_0.User(str_0, str_0)
    assert f'{type(user_0).__module__}.{type(user_0).__qualname__}' == 'snippet_264.User'
    assert user_0.id == 't~BO 4u~j:Z\n'
    assert user_0.name == 't~BO 4u~j:Z\n'
    assert user_0.roles == []

def test_case_2():
    str_0 = '_pJ]+7 ,"y"S'
    user_0 = module_0.User(str_0, str_0)
    assert f'{type(user_0).__module__}.{type(user_0).__qualname__}' == 'snippet_264.User'
    assert user_0.id == '_pJ]+7 ,"y"S'
    assert user_0.name == '_pJ]+7 ,"y"S'
    assert user_0.roles == []
    str_1 = user_0.__repr__()
    assert str_1 == 'User(id=\'_pJ]+7 ,"y"S\', name=\'_pJ]+7 ,"y"S\', roles=[])'