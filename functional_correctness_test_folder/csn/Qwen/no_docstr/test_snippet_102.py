import pytest
import snippet_102 as module_0

def test_case_0():
    bool_0 = False
    expiring_cache_0 = module_0.ExpiringCache(bool_0)
    assert f'{type(expiring_cache_0).__module__}.{type(expiring_cache_0).__qualname__}' == 'snippet_102.ExpiringCache'
    assert expiring_cache_0.duration is False
    assert expiring_cache_0.value is None
    assert expiring_cache_0.deadline == pytest.approx(1758852752.4376268, abs=0.01, rel=0.01)
    expiring_cache_0.get()

def test_case_1():
    bool_0 = True
    expiring_cache_0 = module_0.ExpiringCache(bool_0)
    assert f'{type(expiring_cache_0).__module__}.{type(expiring_cache_0).__qualname__}' == 'snippet_102.ExpiringCache'
    assert expiring_cache_0.duration is True
    assert expiring_cache_0.value is None
    assert expiring_cache_0.deadline == pytest.approx(1758852753.438056, abs=0.01, rel=0.01)
    expiring_cache_0.get()

def test_case_2():
    bool_0 = False
    expiring_cache_0 = module_0.ExpiringCache(bool_0)
    assert f'{type(expiring_cache_0).__module__}.{type(expiring_cache_0).__qualname__}' == 'snippet_102.ExpiringCache'
    assert expiring_cache_0.duration is False
    assert expiring_cache_0.value is None
    assert expiring_cache_0.deadline == pytest.approx(1758852752.438325, abs=0.01, rel=0.01)