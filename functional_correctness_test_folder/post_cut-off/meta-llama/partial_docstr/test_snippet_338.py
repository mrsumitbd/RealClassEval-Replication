import pytest
import snippet_338 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    rate_limiter_0 = module_0.RateLimiter(bool_0)
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_338.RateLimiter'
    assert rate_limiter_0.max_calls is False
    assert rate_limiter_0.period == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert rate_limiter_0.calls == []
    assert f'{type(rate_limiter_0.lock).__module__}.{type(rate_limiter_0.lock).__qualname__}' == '_thread.lock'
    rate_limiter_0.wait()

def test_case_1():
    rate_limiter_0 = module_0.RateLimiter()
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_338.RateLimiter'
    assert rate_limiter_0.max_calls == 3
    assert rate_limiter_0.period == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert rate_limiter_0.calls == []
    assert f'{type(rate_limiter_0.lock).__module__}.{type(rate_limiter_0.lock).__qualname__}' == '_thread.lock'
    var_0 = rate_limiter_0.wait()
    assert f'{type(rate_limiter_0.calls).__module__}.{type(rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(rate_limiter_0.calls) == 1

def test_case_2():
    rate_limiter_0 = module_0.RateLimiter()
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_338.RateLimiter'
    assert rate_limiter_0.max_calls == 3
    assert rate_limiter_0.period == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert rate_limiter_0.calls == []
    assert f'{type(rate_limiter_0.lock).__module__}.{type(rate_limiter_0.lock).__qualname__}' == '_thread.lock'
    var_0 = rate_limiter_0.wait()
    assert f'{type(rate_limiter_0.calls).__module__}.{type(rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(rate_limiter_0.calls) == 1
    var_1 = rate_limiter_0.wait()
    assert len(rate_limiter_0.calls) == 2

def test_case_3():
    rate_limiter_0 = module_0.RateLimiter()
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_338.RateLimiter'
    assert rate_limiter_0.max_calls == 3
    assert rate_limiter_0.period == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert rate_limiter_0.calls == []
    assert f'{type(rate_limiter_0.lock).__module__}.{type(rate_limiter_0.lock).__qualname__}' == '_thread.lock'
    var_0 = rate_limiter_0.wait()
    assert f'{type(rate_limiter_0.calls).__module__}.{type(rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(rate_limiter_0.calls) == 1
    var_1 = rate_limiter_0.wait()
    assert len(rate_limiter_0.calls) == 2
    var_2 = rate_limiter_0.wait()
    assert len(rate_limiter_0.calls) == 3
    var_3 = rate_limiter_0.wait()
    assert len(rate_limiter_0.calls) == 1

@pytest.mark.xfail(strict=True)
def test_case_4():
    bool_0 = False
    rate_limiter_0 = module_0.RateLimiter(period=bool_0)
    assert f'{type(rate_limiter_0).__module__}.{type(rate_limiter_0).__qualname__}' == 'snippet_338.RateLimiter'
    assert rate_limiter_0.max_calls == 3
    assert rate_limiter_0.period is False
    assert rate_limiter_0.calls == []
    assert f'{type(rate_limiter_0.lock).__module__}.{type(rate_limiter_0.lock).__qualname__}' == '_thread.lock'
    bool_1 = False
    rate_limiter_1 = module_0.RateLimiter(bool_1)
    assert f'{type(rate_limiter_1).__module__}.{type(rate_limiter_1).__qualname__}' == 'snippet_338.RateLimiter'
    assert rate_limiter_1.max_calls is False
    assert rate_limiter_1.period == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert rate_limiter_1.calls == []
    assert f'{type(rate_limiter_1.lock).__module__}.{type(rate_limiter_1.lock).__qualname__}' == '_thread.lock'
    var_0 = rate_limiter_0.wait()
    assert f'{type(rate_limiter_0.calls).__module__}.{type(rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(rate_limiter_0.calls) == 1
    rate_limiter_0.wait()
    rate_limiter_1.wait()