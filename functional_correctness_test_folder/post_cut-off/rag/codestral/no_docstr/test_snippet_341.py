import snippet_341 as module_0

def test_case_0():
    bool_0 = False
    free_0 = module_0.Free(bool_0)
    assert f'{type(free_0).__module__}.{type(free_0).__qualname__}' == 'snippet_341.Free'
    assert free_0.guess is False
    var_0 = free_0.__repr__()
    assert var_0 == 'Free(False)'