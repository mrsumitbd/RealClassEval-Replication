import snippet_345 as module_0

def test_case_0():
    str_0 = '}0+&7-P\x0c?Hop.;`=f'
    enhanced_user_0 = module_0.EnhancedUser(str_0, member_openid=str_0)
    assert f'{type(enhanced_user_0).__module__}.{type(enhanced_user_0).__qualname__}' == 'snippet_345.EnhancedUser'
    assert enhanced_user_0.id == '}0+&7-P\x0c?Hop.;`=f'
    assert enhanced_user_0.username is None
    assert enhanced_user_0.avatar is None
    assert enhanced_user_0.bot is None
    assert enhanced_user_0.openid is None
    assert enhanced_user_0.user_openid is None
    assert enhanced_user_0.member_openid == '}0+&7-P\x0c?Hop.;`=f'
    assert module_0.EnhancedUser.id is None
    assert module_0.EnhancedUser.username is None
    assert module_0.EnhancedUser.avatar is None
    assert module_0.EnhancedUser.bot is None
    assert module_0.EnhancedUser.openid is None
    assert module_0.EnhancedUser.user_openid is None
    assert module_0.EnhancedUser.member_openid is None
    assert f'{type(module_0.EnhancedUser.from_dict).__module__}.{type(module_0.EnhancedUser.from_dict).__qualname__}' == 'builtins.method'
    var_0 = enhanced_user_0.get_user_id()
    assert var_0 == '}0+&7-P\x0c?Hop.;`=f'

def test_case_1():
    enhanced_user_0 = module_0.EnhancedUser()
    assert f'{type(enhanced_user_0).__module__}.{type(enhanced_user_0).__qualname__}' == 'snippet_345.EnhancedUser'
    assert enhanced_user_0.id is None
    assert enhanced_user_0.username is None
    assert enhanced_user_0.avatar is None
    assert enhanced_user_0.bot is None
    assert enhanced_user_0.openid is None
    assert enhanced_user_0.user_openid is None
    assert enhanced_user_0.member_openid is None
    assert module_0.EnhancedUser.id is None
    assert module_0.EnhancedUser.username is None
    assert module_0.EnhancedUser.avatar is None
    assert module_0.EnhancedUser.bot is None
    assert module_0.EnhancedUser.openid is None
    assert module_0.EnhancedUser.user_openid is None
    assert module_0.EnhancedUser.member_openid is None
    assert f'{type(module_0.EnhancedUser.from_dict).__module__}.{type(module_0.EnhancedUser.from_dict).__qualname__}' == 'builtins.method'
    enhanced_user_0.get_user_id()

def test_case_2():
    str_0 = 'zC-Iw47g"S`mc'
    enhanced_user_0 = module_0.EnhancedUser(openid=str_0, user_openid=str_0)
    assert f'{type(enhanced_user_0).__module__}.{type(enhanced_user_0).__qualname__}' == 'snippet_345.EnhancedUser'
    assert enhanced_user_0.id is None
    assert enhanced_user_0.username is None
    assert enhanced_user_0.avatar is None
    assert enhanced_user_0.bot is None
    assert enhanced_user_0.openid == 'zC-Iw47g"S`mc'
    assert enhanced_user_0.user_openid == 'zC-Iw47g"S`mc'
    assert enhanced_user_0.member_openid is None
    assert module_0.EnhancedUser.id is None
    assert module_0.EnhancedUser.username is None
    assert module_0.EnhancedUser.avatar is None
    assert module_0.EnhancedUser.bot is None
    assert module_0.EnhancedUser.openid is None
    assert module_0.EnhancedUser.user_openid is None
    assert module_0.EnhancedUser.member_openid is None
    assert f'{type(module_0.EnhancedUser.from_dict).__module__}.{type(module_0.EnhancedUser.from_dict).__qualname__}' == 'builtins.method'
    var_0 = enhanced_user_0.get_user_id()
    assert var_0 == 'zC-Iw47g"S`mc'

def test_case_3():
    str_0 = 'k# \x0bp\t y'
    enhanced_user_0 = module_0.EnhancedUser(avatar=str_0, member_openid=str_0)
    assert f'{type(enhanced_user_0).__module__}.{type(enhanced_user_0).__qualname__}' == 'snippet_345.EnhancedUser'
    assert enhanced_user_0.id is None
    assert enhanced_user_0.username is None
    assert enhanced_user_0.avatar == 'k# \x0bp\t y'
    assert enhanced_user_0.bot is None
    assert enhanced_user_0.openid is None
    assert enhanced_user_0.user_openid is None
    assert enhanced_user_0.member_openid == 'k# \x0bp\t y'
    assert module_0.EnhancedUser.id is None
    assert module_0.EnhancedUser.username is None
    assert module_0.EnhancedUser.avatar is None
    assert module_0.EnhancedUser.bot is None
    assert module_0.EnhancedUser.openid is None
    assert module_0.EnhancedUser.user_openid is None
    assert module_0.EnhancedUser.member_openid is None
    assert f'{type(module_0.EnhancedUser.from_dict).__module__}.{type(module_0.EnhancedUser.from_dict).__qualname__}' == 'builtins.method'
    var_0 = enhanced_user_0.get_user_id()
    assert var_0 == 'k# \x0bp\t y'