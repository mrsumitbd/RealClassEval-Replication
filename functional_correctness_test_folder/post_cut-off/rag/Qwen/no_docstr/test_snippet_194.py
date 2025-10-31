import snippet_194 as module_0

def test_case_0():
    constant_delay_retry_policy_0 = module_0.ConstantDelayRetryPolicy()
    assert f'{type(constant_delay_retry_policy_0).__module__}.{type(constant_delay_retry_policy_0).__qualname__}' == 'snippet_194.ConstantDelayRetryPolicy'
    assert constant_delay_retry_policy_0.maximum_attempts == 3
    assert constant_delay_retry_policy_0.delay == 5
    int_0 = 1722
    list_0 = [constant_delay_retry_policy_0, int_0]
    constant_delay_retry_policy_0.next(constant_delay_retry_policy_0, int_0, list_0)

def test_case_1():
    float_0 = -572.39
    constant_delay_retry_policy_0 = module_0.ConstantDelayRetryPolicy()
    assert f'{type(constant_delay_retry_policy_0).__module__}.{type(constant_delay_retry_policy_0).__qualname__}' == 'snippet_194.ConstantDelayRetryPolicy'
    assert constant_delay_retry_policy_0.maximum_attempts == 3
    assert constant_delay_retry_policy_0.delay == 5
    constant_delay_retry_policy_1 = module_0.ConstantDelayRetryPolicy(delay=constant_delay_retry_policy_0)
    assert f'{type(constant_delay_retry_policy_1).__module__}.{type(constant_delay_retry_policy_1).__qualname__}' == 'snippet_194.ConstantDelayRetryPolicy'
    assert constant_delay_retry_policy_1.maximum_attempts == 3
    assert f'{type(constant_delay_retry_policy_1.delay).__module__}.{type(constant_delay_retry_policy_1.delay).__qualname__}' == 'snippet_194.ConstantDelayRetryPolicy'
    var_0 = constant_delay_retry_policy_1.next(float_0, float_0, float_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_194.ConstantDelayRetryPolicy'
    assert var_0.maximum_attempts == 3
    assert var_0.delay == 5

def test_case_2():
    constant_delay_retry_policy_0 = module_0.ConstantDelayRetryPolicy()
    assert f'{type(constant_delay_retry_policy_0).__module__}.{type(constant_delay_retry_policy_0).__qualname__}' == 'snippet_194.ConstantDelayRetryPolicy'
    assert constant_delay_retry_policy_0.maximum_attempts == 3
    assert constant_delay_retry_policy_0.delay == 5