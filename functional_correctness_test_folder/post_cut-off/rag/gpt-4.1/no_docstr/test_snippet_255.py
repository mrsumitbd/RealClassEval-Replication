import snippet_255 as module_0

def test_case_0():
    bytes_0 = b'\xca\xe38\x16\xb9:\xbc'
    cache_key_builder_0 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_0).__module__}.{type(cache_key_builder_0).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    none_type_0 = None
    cache_key_builder_0.vulnerabilities_key(none_type_0)
    str_0 = ']6<'
    dict_0 = cache_key_builder_0.processes_key(str_0)
    dict_1 = cache_key_builder_0.processes_key(bytes_0, bytes_0)
    cache_key_builder_0.ports_key(dict_1, dict_1)
    cache_key_builder_0.agent_health_key(dict_0)
    none_type_1 = None
    cache_key_builder_0.alerts_key(none_type_1)

def test_case_1():
    cache_key_builder_0 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_0).__module__}.{type(cache_key_builder_0).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    cache_key_builder_0.alerts_key()
    str_0 = ',*n1W`}pJ_Gk*;._.'
    cache_key_builder_0.ports_key(str_0)

def test_case_2():
    cache_key_builder_0 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_0).__module__}.{type(cache_key_builder_0).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    str_0 = '8yY}]rr4}=0q$iDii|'
    none_type_0 = None
    cache_key_builder_0.ports_key(str_0, none_type_0, str_0)

def test_case_3():
    str_0 = "VY*\\'}0"
    cache_key_builder_0 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_0).__module__}.{type(cache_key_builder_0).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    cache_key_builder_0.alerts_key(time_range=str_0)

def test_case_4():
    cache_key_builder_0 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_0).__module__}.{type(cache_key_builder_0).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    dict_0 = cache_key_builder_0.vulnerabilities_key()
    cache_key_builder_0.alerts_key(dict_0)
    str_0 = 'pcT7%XIZ*B,'
    cache_key_builder_0.agent_health_key(str_0)

def test_case_5():
    str_0 = '&&@8Ph'
    cache_key_builder_0 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_0).__module__}.{type(cache_key_builder_0).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    cache_key_builder_0.processes_key(str_0)
    cache_key_builder_1 = module_0.CacheKeyBuilder()
    assert f'{type(cache_key_builder_1).__module__}.{type(cache_key_builder_1).__qualname__}' == 'snippet_255.CacheKeyBuilder'
    cache_key_builder_1.vulnerabilities_key()