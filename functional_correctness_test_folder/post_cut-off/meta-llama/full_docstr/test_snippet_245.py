import snippet_245 as module_0

def test_case_0():
    callable_registry_0 = module_0.CallableRegistry()
    assert f'{type(callable_registry_0).__module__}.{type(callable_registry_0).__qualname__}' == 'snippet_245.CallableRegistry'
    assert f'{type(module_0.CallableRegistry.register).__module__}.{type(module_0.CallableRegistry.register).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.CallableRegistry.get).__module__}.{type(module_0.CallableRegistry.get).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.CallableRegistry.contains).__module__}.{type(module_0.CallableRegistry.contains).__qualname__}' == 'builtins.method'