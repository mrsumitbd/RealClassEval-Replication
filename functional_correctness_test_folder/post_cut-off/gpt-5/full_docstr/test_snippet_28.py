import pytest
import snippet_28 as module_0
import claude_monitor.core.models as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = 1404
    str_0 = ''
    dict_0 = {}
    dict_1 = {str_0: dict_0}
    pricing_calculator_0 = module_0.PricingCalculator(dict_1)
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert pricing_calculator_0.pricing == {'': {}}
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    pricing_calculator_0.calculate_cost(int_0, output_tokens=int_0)

def test_case_1():
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3

@pytest.mark.xfail(strict=True)
def test_case_2():
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    int_0 = -2350
    pricing_calculator_0.calculate_cost(pricing_calculator_0, int_0, int_0, strict=int_0)

def test_case_3():
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    str_0 = 'Q<!\n@;'
    bool_0 = False
    float_0 = pricing_calculator_0.calculate_cost(str_0, bool_0)
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)

def test_case_4():
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    dict_0 = {pricing_calculator_0: pricing_calculator_0, pricing_calculator_0: pricing_calculator_0, pricing_calculator_0: pricing_calculator_0, pricing_calculator_0: pricing_calculator_0}
    cost_mode_0 = module_1.CostMode.CACHED
    with pytest.raises(KeyError):
        pricing_calculator_0.calculate_cost_for_entry(dict_0, cost_mode_0)

def test_case_5():
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    str_0 = 'B+aS2q(BV\\T*F{'
    dict_0 = {str_0: pricing_calculator_0, str_0: str_0}
    cost_mode_0 = module_1.CostMode.AUTO
    with pytest.raises(KeyError):
        pricing_calculator_0.calculate_cost_for_entry(dict_0, cost_mode_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    none_type_0 = None
    pricing_calculator_0 = module_0.PricingCalculator(none_type_0)
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    int_0 = 3525
    pricing_calculator_0.calculate_cost(pricing_calculator_0, pricing_calculator_0, cache_creation_tokens=int_0, tokens=pricing_calculator_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    none_type_0 = None
    str_0 = 'ZX'
    bool_0 = False
    bool_1 = True
    pricing_calculator_1 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_1).__module__}.{type(pricing_calculator_1).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_1.pricing).__module__}.{type(pricing_calculator_1.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_1.pricing) == 7
    pricing_calculator_0.calculate_cost(str_0, output_tokens=bool_0, cache_read_tokens=bool_1, tokens=none_type_0, strict=pricing_calculator_1)

def test_case_8():
    str_0 = "+:ZNdB6='\x0bk^_"
    pricing_calculator_0 = module_0.PricingCalculator()
    assert f'{type(pricing_calculator_0).__module__}.{type(pricing_calculator_0).__qualname__}' == 'snippet_28.PricingCalculator'
    assert f'{type(pricing_calculator_0.pricing).__module__}.{type(pricing_calculator_0.pricing).__qualname__}' == 'builtins.dict'
    assert len(pricing_calculator_0.pricing) == 7
    assert f'{type(module_0.PricingCalculator.FALLBACK_PRICING).__module__}.{type(module_0.PricingCalculator.FALLBACK_PRICING).__qualname__}' == 'builtins.dict'
    assert len(module_0.PricingCalculator.FALLBACK_PRICING) == 3
    str_1 = "OX\nJa'`AlbW\x0bHfB"
    none_type_0 = None
    float_0 = pricing_calculator_0.calculate_cost(str_1, tokens=none_type_0)
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)
    dict_0 = {str_0: str_0, str_0: str_0, str_0: str_0}
    float_1 = pricing_calculator_0.calculate_cost(str_1, strict=none_type_0)
    assert float_1 == pytest.approx(0.0, abs=0.01, rel=0.01)
    cost_mode_0 = module_1.CostMode.CACHED
    with pytest.raises(KeyError):
        pricing_calculator_0.calculate_cost_for_entry(dict_0, cost_mode_0)