import pytest
import snippet_220 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    rate_limits_info_0 = module_0.RateLimitsInfo()
    assert f'{type(rate_limits_info_0).__module__}.{type(rate_limits_info_0).__qualname__}' == 'snippet_220.RateLimitsInfo'
    assert module_0.RateLimitsInfo.interval is None
    assert module_0.RateLimitsInfo.limit is None
    assert module_0.RateLimitsInfo.remaining is None
    assert module_0.RateLimitsInfo.reset is None
    assert module_0.RateLimitsInfo.throttled is None
    assert f'{type(module_0.RateLimitsInfo.from_dict).__module__}.{type(module_0.RateLimitsInfo.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RateLimitsInfo.from_headers).__module__}.{type(module_0.RateLimitsInfo.from_headers).__qualname__}' == 'builtins.method'
    rate_limits_info_0.__str__()