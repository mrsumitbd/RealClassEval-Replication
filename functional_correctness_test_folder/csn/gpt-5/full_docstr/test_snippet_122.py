import snippet_122 as module_0

def test_case_0():
    int_0 = 901
    rate_limit_0 = module_0.RateLimit(limit=int_0, remaining=int_0, reset_epoch=int_0)
    assert f'{type(rate_limit_0).__module__}.{type(rate_limit_0).__qualname__}' == 'snippet_122.RateLimit'
    assert rate_limit_0.limit == 901
    assert rate_limit_0.remaining == 901
    assert f'{type(rate_limit_0.reset_datetime).__module__}.{type(rate_limit_0.reset_datetime).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_0.RateLimit.from_http).__module__}.{type(module_0.RateLimit.from_http).__qualname__}' == 'builtins.method'
    bool_0 = rate_limit_0.__bool__()
    assert bool_0 is True

def test_case_1():
    int_0 = -2143
    rate_limit_0 = module_0.RateLimit(limit=int_0, remaining=int_0, reset_epoch=int_0)
    assert f'{type(rate_limit_0).__module__}.{type(rate_limit_0).__qualname__}' == 'snippet_122.RateLimit'
    assert rate_limit_0.limit == -2143
    assert rate_limit_0.remaining == -2143
    assert f'{type(rate_limit_0.reset_datetime).__module__}.{type(rate_limit_0.reset_datetime).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_0.RateLimit.from_http).__module__}.{type(module_0.RateLimit.from_http).__qualname__}' == 'builtins.method'
    bool_0 = rate_limit_0.__bool__()
    assert bool_0 is True

def test_case_2():
    int_0 = -2143
    rate_limit_0 = module_0.RateLimit(limit=int_0, remaining=int_0, reset_epoch=int_0)
    assert f'{type(rate_limit_0).__module__}.{type(rate_limit_0).__qualname__}' == 'snippet_122.RateLimit'
    assert rate_limit_0.limit == -2143
    assert rate_limit_0.remaining == -2143
    assert f'{type(rate_limit_0.reset_datetime).__module__}.{type(rate_limit_0.reset_datetime).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_0.RateLimit.from_http).__module__}.{type(module_0.RateLimit.from_http).__qualname__}' == 'builtins.method'

def test_case_3():
    int_0 = 805
    rate_limit_0 = module_0.RateLimit(limit=int_0, remaining=int_0, reset_epoch=int_0)
    assert f'{type(rate_limit_0).__module__}.{type(rate_limit_0).__qualname__}' == 'snippet_122.RateLimit'
    assert rate_limit_0.limit == 805
    assert rate_limit_0.remaining == 805
    assert f'{type(rate_limit_0.reset_datetime).__module__}.{type(rate_limit_0.reset_datetime).__qualname__}' == 'datetime.datetime'
    assert f'{type(module_0.RateLimit.from_http).__module__}.{type(module_0.RateLimit.from_http).__qualname__}' == 'builtins.method'
    str_0 = rate_limit_0.__str__()
    assert str_0 == '< 805/805 until 1970-01-01 00:13:25+00:00 >'
    bool_0 = rate_limit_0.__bool__()
    assert bool_0 is True