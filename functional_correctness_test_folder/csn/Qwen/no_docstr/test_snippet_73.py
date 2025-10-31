import pytest
import snippet_73 as module_0

def test_case_0():
    sentinel_hub_rate_limit_0 = module_0.SentinelHubRateLimit()
    assert f'{type(sentinel_hub_rate_limit_0).__module__}.{type(sentinel_hub_rate_limit_0).__qualname__}' == 'snippet_73.SentinelHubRateLimit'
    assert sentinel_hub_rate_limit_0.wait_time == pytest.approx(0.05, abs=0.01, rel=0.01)
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.31491725, abs=0.01, rel=0.01)
    assert module_0.SentinelHubRateLimit.RETRY_HEADER == 'Retry-After'
    assert module_0.SentinelHubRateLimit.UNITS_SPENT_HEADER == 'X-ProcessingUnits-Spent'
    float_0 = sentinel_hub_rate_limit_0.register_next()
    assert float_0 == 0
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.365067291, abs=0.01, rel=0.01)

def test_case_1():
    bool_0 = True
    sentinel_hub_rate_limit_0 = module_0.SentinelHubRateLimit(bool_0, maximum_wait_time=bool_0)
    assert f'{type(sentinel_hub_rate_limit_0).__module__}.{type(sentinel_hub_rate_limit_0).__qualname__}' == 'snippet_73.SentinelHubRateLimit'
    assert sentinel_hub_rate_limit_0.wait_time == pytest.approx(0.05, abs=0.01, rel=0.01)
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.315312916, abs=0.01, rel=0.01)
    assert module_0.SentinelHubRateLimit.RETRY_HEADER == 'Retry-After'
    assert module_0.SentinelHubRateLimit.UNITS_SPENT_HEADER == 'X-ProcessingUnits-Spent'
    float_0 = sentinel_hub_rate_limit_0.register_next()
    assert float_0 == 0
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.365430416, abs=0.01, rel=0.01)
    float_1 = sentinel_hub_rate_limit_0.register_next()
    assert float_1 == pytest.approx(0.04992900000070222, abs=0.01, rel=0.01)

def test_case_2():
    dict_0 = {}
    sentinel_hub_rate_limit_0 = module_0.SentinelHubRateLimit()
    assert f'{type(sentinel_hub_rate_limit_0).__module__}.{type(sentinel_hub_rate_limit_0).__qualname__}' == 'snippet_73.SentinelHubRateLimit'
    assert sentinel_hub_rate_limit_0.wait_time == pytest.approx(0.05, abs=0.01, rel=0.01)
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.315727333, abs=0.01, rel=0.01)
    assert module_0.SentinelHubRateLimit.RETRY_HEADER == 'Retry-After'
    assert module_0.SentinelHubRateLimit.UNITS_SPENT_HEADER == 'X-ProcessingUnits-Spent'
    float_0 = sentinel_hub_rate_limit_0.register_next()
    assert float_0 == 0
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.365792291, abs=0.01, rel=0.01)
    float_1 = -2182.68
    int_0 = 4127
    sentinel_hub_rate_limit_1 = module_0.SentinelHubRateLimit(int_0)
    assert f'{type(sentinel_hub_rate_limit_1).__module__}.{type(sentinel_hub_rate_limit_1).__qualname__}' == 'snippet_73.SentinelHubRateLimit'
    assert sentinel_hub_rate_limit_1.wait_time == pytest.approx(60.0, abs=0.01, rel=0.01)
    assert sentinel_hub_rate_limit_1.next_download_time == pytest.approx(91036.315891875, abs=0.01, rel=0.01)
    sentinel_hub_rate_limit_1.update(dict_0, default=float_1)

def test_case_3():
    int_0 = 28
    sentinel_hub_rate_limit_0 = module_0.SentinelHubRateLimit(int_0, maximum_wait_time=int_0)
    assert f'{type(sentinel_hub_rate_limit_0).__module__}.{type(sentinel_hub_rate_limit_0).__qualname__}' == 'snippet_73.SentinelHubRateLimit'
    assert sentinel_hub_rate_limit_0.wait_time == pytest.approx(1.4000000000000001, abs=0.01, rel=0.01)
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91036.316271791, abs=0.01, rel=0.01)
    assert module_0.SentinelHubRateLimit.RETRY_HEADER == 'Retry-After'
    assert module_0.SentinelHubRateLimit.UNITS_SPENT_HEADER == 'X-ProcessingUnits-Spent'
    float_0 = sentinel_hub_rate_limit_0.register_next()
    assert float_0 == 0
    assert sentinel_hub_rate_limit_0.next_download_time == pytest.approx(91037.71633820799, abs=0.01, rel=0.01)
    none_type_0 = None
    dict_0 = {float_0: float_0, none_type_0: none_type_0, sentinel_hub_rate_limit_0: int_0}
    sentinel_hub_rate_limit_0.update(dict_0, default=float_0)