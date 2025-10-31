import pytest
import snippet_165 as module_0
import mgz.model.definitions as module_1

def test_case_0():
    bool_0 = False
    inputs_0 = module_0.Inputs(bool_0)
    assert f'{type(inputs_0).__module__}.{type(inputs_0).__qualname__}' == 'snippet_165.Inputs'
    assert inputs_0.inputs == []

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    inputs_0 = module_0.Inputs(bool_0)
    assert f'{type(inputs_0).__module__}.{type(inputs_0).__qualname__}' == 'snippet_165.Inputs'
    assert inputs_0.inputs == []
    inputs_0.add_chat(inputs_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    list_0 = []
    bool_0 = False
    inputs_0 = module_0.Inputs(bool_0)
    assert f'{type(inputs_0).__module__}.{type(inputs_0).__qualname__}' == 'snippet_165.Inputs'
    assert inputs_0.inputs == []
    dict_0 = {}
    input_0 = module_1.Input(inputs_0, bool_0, list_0, dict_0)
    assert f'{type(input_0).__module__}.{type(input_0).__qualname__}' == 'mgz.model.definitions.Input'
    assert f'{type(input_0.timestamp).__module__}.{type(input_0.timestamp).__qualname__}' == 'snippet_165.Inputs'
    assert input_0.type is False
    assert input_0.param == []
    assert input_0.payload == {}
    assert input_0.player is None
    assert input_0.position is None
    assert module_1.Input.player is None
    assert module_1.Input.position is None
    inputs_0.add_action(input_0)