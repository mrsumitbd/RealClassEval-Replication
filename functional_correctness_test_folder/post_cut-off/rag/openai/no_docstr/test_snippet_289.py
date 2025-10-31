import pytest
import snippet_289 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'L+|]B$gxBVL\nj6p'
    bool_0 = True
    module_0.UpdateRuleDeployment(bool_0, detection_exclusion_application=str_0)

def test_case_1():
    update_rule_deployment_0 = module_0.UpdateRuleDeployment()
    assert f'{type(update_rule_deployment_0).__module__}.{type(update_rule_deployment_0).__qualname__}' == 'snippet_289.UpdateRuleDeployment'
    assert update_rule_deployment_0.enabled is None
    assert update_rule_deployment_0.archived is None
    assert update_rule_deployment_0.detection_exclusion_application is None
    assert module_0.UpdateRuleDeployment.enabled is None
    assert module_0.UpdateRuleDeployment.archived is None
    assert module_0.UpdateRuleDeployment.detection_exclusion_application is None

def test_case_2():
    none_type_0 = None
    update_rule_deployment_0 = module_0.UpdateRuleDeployment(archived=none_type_0, detection_exclusion_application=none_type_0)
    assert f'{type(update_rule_deployment_0).__module__}.{type(update_rule_deployment_0).__qualname__}' == 'snippet_289.UpdateRuleDeployment'
    assert update_rule_deployment_0.enabled is None
    assert update_rule_deployment_0.archived is None
    assert update_rule_deployment_0.detection_exclusion_application is None
    assert module_0.UpdateRuleDeployment.enabled is None
    assert module_0.UpdateRuleDeployment.archived is None
    assert module_0.UpdateRuleDeployment.detection_exclusion_application is None
    update_rule_deployment_0.to_dict()

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'L+|]B$gxBVL\nj6p'
    module_0.UpdateRuleDeployment(str_0, detection_exclusion_application=str_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    bool_0 = True
    none_type_0 = None
    module_0.UpdateRuleDeployment(bool_0, bool_0, none_type_0)