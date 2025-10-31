import pytest
import snippet_45 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = -3475
    tuple_0 = (int_0, int_0)
    token_bucket_rate_limiter_0 = module_0.TokenBucketRateLimiter(tuple_0, int_0)
    assert f'{type(token_bucket_rate_limiter_0).__module__}.{type(token_bucket_rate_limiter_0).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_0.tokens_per_second == (-3475, -3475)
    assert token_bucket_rate_limiter_0.bucket_capacity == -3475
    assert token_bucket_rate_limiter_0.tokens == -3475
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.052802, abs=0.01, rel=0.01)
    set_0 = {token_bucket_rate_limiter_0}
    token_bucket_rate_limiter_1 = module_0.TokenBucketRateLimiter(set_0)
    assert f'{type(token_bucket_rate_limiter_1).__module__}.{type(token_bucket_rate_limiter_1).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert f'{type(token_bucket_rate_limiter_1.tokens_per_second).__module__}.{type(token_bucket_rate_limiter_1.tokens_per_second).__qualname__}' == 'builtins.set'
    assert len(token_bucket_rate_limiter_1.tokens_per_second) == 1
    assert f'{type(token_bucket_rate_limiter_1.bucket_capacity).__module__}.{type(token_bucket_rate_limiter_1.bucket_capacity).__qualname__}' == 'builtins.set'
    assert len(token_bucket_rate_limiter_1.bucket_capacity) == 1
    assert f'{type(token_bucket_rate_limiter_1.tokens).__module__}.{type(token_bucket_rate_limiter_1.tokens).__qualname__}' == 'builtins.set'
    assert len(token_bucket_rate_limiter_1.tokens) == 1
    assert token_bucket_rate_limiter_1.last_refill_time == pytest.approx(1758850856.053622, abs=0.01, rel=0.01)
    token_bucket_rate_limiter_1.get_wait_time()

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = 3558
    token_bucket_rate_limiter_0 = module_0.TokenBucketRateLimiter(int_0)
    assert f'{type(token_bucket_rate_limiter_0).__module__}.{type(token_bucket_rate_limiter_0).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_0.tokens_per_second == 3558
    assert token_bucket_rate_limiter_0.bucket_capacity == 3558
    assert token_bucket_rate_limiter_0.tokens == 3558
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.0559201, abs=0.01, rel=0.01)
    token_bucket_rate_limiter_1 = module_0.TokenBucketRateLimiter(token_bucket_rate_limiter_0)
    assert f'{type(token_bucket_rate_limiter_1).__module__}.{type(token_bucket_rate_limiter_1).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert f'{type(token_bucket_rate_limiter_1.tokens_per_second).__module__}.{type(token_bucket_rate_limiter_1.tokens_per_second).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert f'{type(token_bucket_rate_limiter_1.bucket_capacity).__module__}.{type(token_bucket_rate_limiter_1.bucket_capacity).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert f'{type(token_bucket_rate_limiter_1.tokens).__module__}.{type(token_bucket_rate_limiter_1.tokens).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_1.last_refill_time == pytest.approx(1758850856.0564952, abs=0.01, rel=0.01)
    token_bucket_rate_limiter_1.get_wait_time()

@pytest.mark.xfail(strict=True)
def test_case_2():
    bool_0 = True
    token_bucket_rate_limiter_0 = module_0.TokenBucketRateLimiter(bool_0)
    assert f'{type(token_bucket_rate_limiter_0).__module__}.{type(token_bucket_rate_limiter_0).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_0.tokens_per_second is True
    assert token_bucket_rate_limiter_0.bucket_capacity is True
    assert token_bucket_rate_limiter_0.tokens is True
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.057733, abs=0.01, rel=0.01)
    bool_1 = token_bucket_rate_limiter_0.try_consume_token()
    assert bool_1 is True
    assert token_bucket_rate_limiter_0.tokens == 0
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.058039, abs=0.01, rel=0.01)
    bool_2 = False
    token_bucket_rate_limiter_1 = module_0.TokenBucketRateLimiter(bool_2)
    assert f'{type(token_bucket_rate_limiter_1).__module__}.{type(token_bucket_rate_limiter_1).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_1.tokens_per_second is False
    assert token_bucket_rate_limiter_1.bucket_capacity is False
    assert token_bucket_rate_limiter_1.tokens is False
    assert token_bucket_rate_limiter_1.last_refill_time == pytest.approx(1758850856.058422, abs=0.01, rel=0.01)
    token_bucket_rate_limiter_1.get_wait_time()

def test_case_3():
    bool_0 = True
    token_bucket_rate_limiter_0 = module_0.TokenBucketRateLimiter(bool_0)
    assert f'{type(token_bucket_rate_limiter_0).__module__}.{type(token_bucket_rate_limiter_0).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_0.tokens_per_second is True
    assert token_bucket_rate_limiter_0.bucket_capacity is True
    assert token_bucket_rate_limiter_0.tokens is True
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.059723, abs=0.01, rel=0.01)
    bool_1 = token_bucket_rate_limiter_0.try_consume_token()
    assert bool_1 is True
    assert token_bucket_rate_limiter_0.tokens == 0
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.060013, abs=0.01, rel=0.01)
    bool_2 = token_bucket_rate_limiter_0.try_consume_token()
    assert bool_2 is False
    assert token_bucket_rate_limiter_0.tokens == pytest.approx(0.00028896331787109375, abs=0.01, rel=0.01)
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.060302, abs=0.01, rel=0.01)
    float_0 = token_bucket_rate_limiter_0.get_wait_time()
    assert float_0 == pytest.approx(0.999424934387207, abs=0.01, rel=0.01)
    assert token_bucket_rate_limiter_0.tokens == pytest.approx(0.0005750656127929688, abs=0.01, rel=0.01)
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.0605881, abs=0.01, rel=0.01)

def test_case_4():
    bool_0 = True
    token_bucket_rate_limiter_0 = module_0.TokenBucketRateLimiter(bool_0)
    assert f'{type(token_bucket_rate_limiter_0).__module__}.{type(token_bucket_rate_limiter_0).__qualname__}' == 'snippet_45.TokenBucketRateLimiter'
    assert token_bucket_rate_limiter_0.tokens_per_second is True
    assert token_bucket_rate_limiter_0.bucket_capacity is True
    assert token_bucket_rate_limiter_0.tokens is True
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.061415, abs=0.01, rel=0.01)
    float_0 = token_bucket_rate_limiter_0.get_wait_time()
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.061697, abs=0.01, rel=0.01)
    bool_1 = token_bucket_rate_limiter_0.try_consume_token()
    assert bool_1 is True
    assert token_bucket_rate_limiter_0.tokens == 0
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.061981, abs=0.01, rel=0.01)
    bool_2 = token_bucket_rate_limiter_0.try_consume_token()
    assert bool_2 is False
    assert token_bucket_rate_limiter_0.tokens == pytest.approx(0.0002689361572265625, abs=0.01, rel=0.01)
    assert token_bucket_rate_limiter_0.last_refill_time == pytest.approx(1758850856.06225, abs=0.01, rel=0.01)