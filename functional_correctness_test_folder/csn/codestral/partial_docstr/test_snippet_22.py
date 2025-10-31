import pytest
import snippet_22 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = -2270
    base_validation_rules_0 = module_0.BaseValidationRules()
    assert f'{type(base_validation_rules_0).__module__}.{type(base_validation_rules_0).__qualname__}' == 'snippet_22.BaseValidationRules'
    base_validation_rules_0.validate_transaction(int_0, int_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    set_0 = set()
    base_validation_rules_0 = module_0.BaseValidationRules(*set_0)
    assert f'{type(base_validation_rules_0).__module__}.{type(base_validation_rules_0).__qualname__}' == 'snippet_22.BaseValidationRules'
    base_validation_rules_0.validate_block(base_validation_rules_0, set_0)