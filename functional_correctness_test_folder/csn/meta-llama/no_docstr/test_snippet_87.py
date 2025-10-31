import pytest
import snippet_87 as module_0

def test_case_0():
    context_flag_0 = module_0.ContextFlag()
    assert f'{type(context_flag_0).__module__}.{type(context_flag_0).__qualname__}' == 'snippet_87.ContextFlag'
    context_flag_0.__enter__()
    context_flag_0.__exit__()
    with pytest.raises(ValueError):
        context_flag_0.__exit__()

def test_case_1():
    context_flag_0 = module_0.ContextFlag()
    assert f'{type(context_flag_0).__module__}.{type(context_flag_0).__qualname__}' == 'snippet_87.ContextFlag'
    context_flag_0.__enter__()

def test_case_2():
    context_flag_0 = module_0.ContextFlag()
    assert f'{type(context_flag_0).__module__}.{type(context_flag_0).__qualname__}' == 'snippet_87.ContextFlag'
    bool_0 = context_flag_0.__bool__()
    assert bool_0 is False
    context_flag_0.__enter__()