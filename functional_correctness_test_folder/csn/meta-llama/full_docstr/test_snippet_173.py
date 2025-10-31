import pytest
import snippet_173 as module_0
import builtins as module_1

def test_case_0():
    bool_0 = True
    single_thing_0 = module_0.SingleThing(bool_0)
    assert f'{type(single_thing_0).__module__}.{type(single_thing_0).__qualname__}' == 'snippet_173.SingleThing'
    assert single_thing_0.thing is True
    var_0 = single_thing_0.get_thing()
    assert var_0 is True

def test_case_1():
    object_0 = module_1.object()
    single_thing_0 = module_0.SingleThing(object_0)
    assert f'{type(single_thing_0).__module__}.{type(single_thing_0).__qualname__}' == 'snippet_173.SingleThing'
    assert f'{type(single_thing_0.thing).__module__}.{type(single_thing_0.thing).__qualname__}' == 'builtins.object'
    single_thing_0.get_things()

@pytest.mark.xfail(strict=True)
def test_case_2():
    int_0 = 2168
    single_thing_0 = module_0.SingleThing(int_0)
    assert f'{type(single_thing_0).__module__}.{type(single_thing_0).__qualname__}' == 'snippet_173.SingleThing'
    assert single_thing_0.thing == 2168
    single_thing_0.get_name()