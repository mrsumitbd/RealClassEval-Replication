import snippet_151 as module_0

def test_case_0():
    str_0 = 'QO'
    adaptive_card_component_0 = module_0.AdaptiveCardComponent(str_0, str_0)
    assert f'{type(adaptive_card_component_0).__module__}.{type(adaptive_card_component_0).__qualname__}' == 'snippet_151.AdaptiveCardComponent'
    assert adaptive_card_component_0.serializable_properties == 'QO'
    assert adaptive_card_component_0.simple_properties == 'QO'
    var_0 = adaptive_card_component_0.to_json()
    assert var_0 == '{}'

def test_case_1():
    int_0 = -618
    adaptive_card_component_0 = module_0.AdaptiveCardComponent(int_0, int_0)
    assert f'{type(adaptive_card_component_0).__module__}.{type(adaptive_card_component_0).__qualname__}' == 'snippet_151.AdaptiveCardComponent'
    assert adaptive_card_component_0.serializable_properties == -618
    assert adaptive_card_component_0.simple_properties == -618