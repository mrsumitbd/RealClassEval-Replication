import snippet_147 as module_0

def test_case_0():
    none_type_0 = None
    no_hash_context_0 = module_0.NoHashContext()
    assert f'{type(no_hash_context_0).__module__}.{type(no_hash_context_0).__qualname__}' == 'snippet_147.NoHashContext'
    no_hash_context_0.update(none_type_0)

def test_case_1():
    no_hash_context_0 = module_0.NoHashContext()
    assert f'{type(no_hash_context_0).__module__}.{type(no_hash_context_0).__qualname__}' == 'snippet_147.NoHashContext'
    no_hash_context_0.digest()

def test_case_2():
    none_type_0 = None
    no_hash_context_0 = module_0.NoHashContext(none_type_0)
    assert f'{type(no_hash_context_0).__module__}.{type(no_hash_context_0).__qualname__}' == 'snippet_147.NoHashContext'
    no_hash_context_0.digest()
    no_hash_context_0.hexdigest()