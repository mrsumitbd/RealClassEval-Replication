import pytest
import snippet_356 as module_0

def test_case_0():
    str_0 = '0O~-=R!Ptv;Y4Iz]3'
    callable_compose_0 = module_0.CallableCompose(str_0)
    assert f'{type(callable_compose_0).__module__}.{type(callable_compose_0).__qualname__}' == 'snippet_356.CallableCompose'
    assert callable_compose_0.callables == '0O~-=R!Ptv;Y4Iz]3'
    with pytest.raises(TypeError):
        callable_compose_0.__call__()

def test_case_1():
    set_0 = set()
    callable_compose_0 = module_0.CallableCompose(set_0)
    assert f'{type(callable_compose_0).__module__}.{type(callable_compose_0).__qualname__}' == 'snippet_356.CallableCompose'
    assert callable_compose_0.callables == {*()}
    with pytest.raises(ValueError):
        callable_compose_0.__call__()

def test_case_2():
    int_0 = -174
    callable_compose_0 = module_0.CallableCompose(int_0)
    assert f'{type(callable_compose_0).__module__}.{type(callable_compose_0).__qualname__}' == 'snippet_356.CallableCompose'
    assert callable_compose_0.callables == -174

def test_case_3():
    str_0 = ']Nb(k#6A\rv1}9ea=BR%'
    dict_0 = {str_0: str_0, str_0: str_0, str_0: str_0, str_0: str_0}
    bool_0 = True
    callable_compose_0 = module_0.CallableCompose(bool_0)
    assert f'{type(callable_compose_0).__module__}.{type(callable_compose_0).__qualname__}' == 'snippet_356.CallableCompose'
    assert callable_compose_0.callables is True
    dict_1 = {callable_compose_0: bool_0, bool_0: bool_0, bool_0: bool_0, callable_compose_0: callable_compose_0}
    callable_compose_1 = module_0.CallableCompose(dict_1)
    assert f'{type(callable_compose_1).__module__}.{type(callable_compose_1).__qualname__}' == 'snippet_356.CallableCompose'
    assert f'{type(callable_compose_1.callables).__module__}.{type(callable_compose_1.callables).__qualname__}' == 'builtins.dict'
    assert len(callable_compose_1.callables) == 2
    with pytest.raises(RuntimeError):
        callable_compose_1.__call__(**dict_0)