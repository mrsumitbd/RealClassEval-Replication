import pytest
import snippet_189 as module_0

def test_case_0():
    int_0 = 2035
    rate_limiter_0 = module_0.RateLimiter(int_0)
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_189.RateLimiter'
    assert rate_limiter_0.hz == 2035
    assert rate_limiter_0.last_time == pytest.approx(1758904345.518941, abs=0.01, rel=0.01)
    assert rate_limiter_0.sleep_duration == pytest.approx(0.0004914004914004914, abs=0.01, rel=0.01)
    assert rate_limiter_0.render_period == pytest.approx(0.0004914004914004914, abs=0.01, rel=0.01)
    rate_limiter_0.sleep(int_0)
    assert rate_limiter_0.last_time == pytest.approx(1758904345.5199237, abs=0.01, rel=0.01)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    module_0.RateLimiter(bool_0)

def test_case_2():
    int_0 = 2035
    rate_limiter_0 = module_0.RateLimiter(int_0)
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_189.RateLimiter'
    assert rate_limiter_0.hz == 2035
    assert rate_limiter_0.last_time == pytest.approx(1758904345.520853, abs=0.01, rel=0.01)
    assert rate_limiter_0.sleep_duration == pytest.approx(0.0004914004914004914, abs=0.01, rel=0.01)
    assert rate_limiter_0.render_period == pytest.approx(0.0004914004914004914, abs=0.01, rel=0.01)
    none_type_0 = None
    rate_limiter_0.sleep(none_type_0)

def test_case_3():
    int_0 = 870
    int_1 = 3652
    rate_limiter_0 = module_0.RateLimiter(int_1)
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_189.RateLimiter'
    assert rate_limiter_0.hz == 3652
    assert rate_limiter_0.last_time == pytest.approx(1758904345.522639, abs=0.01, rel=0.01)
    assert rate_limiter_0.sleep_duration == pytest.approx(0.0002738225629791895, abs=0.01, rel=0.01)
    assert rate_limiter_0.render_period == pytest.approx(0.0002738225629791895, abs=0.01, rel=0.01)
    rate_limiter_0.sleep(int_0)
    assert rate_limiter_0.last_time == pytest.approx(1758904345.5231864, abs=0.01, rel=0.01)