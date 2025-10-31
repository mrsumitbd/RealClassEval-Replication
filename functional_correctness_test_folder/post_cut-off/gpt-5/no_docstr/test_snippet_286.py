import snippet_286 as module_0

def test_case_0():
    str_0 = ';Os.pK(99\rm'
    navigation_action_0 = module_0.NavigationAction(str_0)
    assert f'{type(navigation_action_0).__module__}.{type(navigation_action_0).__qualname__}' == 'snippet_286.NavigationAction'
    assert navigation_action_0.target_uri == ';Os.pK(99\rm'

def test_case_1():
    str_0 = '!\tbF8GB8ICrq(\r^Nh>'
    navigation_action_0 = module_0.NavigationAction(str_0)
    assert f'{type(navigation_action_0).__module__}.{type(navigation_action_0).__qualname__}' == 'snippet_286.NavigationAction'
    assert navigation_action_0.target_uri == '!\tbF8GB8ICrq(\r^Nh>'
    str_1 = navigation_action_0.__repr__()
    assert str_1 == 'NavigationAction(target_uri=!\tbF8GB8ICrq(\r^Nh>)'