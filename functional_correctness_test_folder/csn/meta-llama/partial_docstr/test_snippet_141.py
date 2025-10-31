import snippet_141 as module_0
import functools as module_1

def test_case_0():
    bool_0 = True
    api_0 = module_0.Api()
    assert f'{type(api_0).__module__}.{type(api_0).__qualname__}' == 'snippet_141.Api'
    api_0.call_action(bool_0)

def test_case_1():
    api_0 = module_0.Api()
    assert f'{type(api_0).__module__}.{type(api_0).__qualname__}' == 'snippet_141.Api'
    str_0 = '+x;\r'
    callable_0 = api_0.__getattr__(str_0)
    assert f'{type(callable_0).__module__}.{type(callable_0).__qualname__}' == 'functools.partial'
    assert f'{type(module_1.partial.func).__module__}.{type(module_1.partial.func).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.partial.args).__module__}.{type(module_1.partial.args).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.partial.keywords).__module__}.{type(module_1.partial.keywords).__qualname__}' == 'builtins.member_descriptor'