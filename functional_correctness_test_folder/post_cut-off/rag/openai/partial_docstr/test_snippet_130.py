import pytest
import snippet_130 as module_0

def test_case_0():
    bool_0 = True
    bounded_a_s_t_cache_0 = module_0.BoundedASTCache()
    assert f'{type(bounded_a_s_t_cache_0).__module__}.{type(bounded_a_s_t_cache_0).__qualname__}' == 'snippet_130.BoundedASTCache'
    assert f'{type(bounded_a_s_t_cache_0.cache).__module__}.{type(bounded_a_s_t_cache_0.cache).__qualname__}' == 'collections.OrderedDict'
    assert len(bounded_a_s_t_cache_0.cache) == 0
    assert bounded_a_s_t_cache_0.max_entries == 1000
    assert bounded_a_s_t_cache_0.max_memory_bytes == 524288000
    none_type_0 = bounded_a_s_t_cache_0.__setitem__(bool_0, bool_0)
    assert len(bounded_a_s_t_cache_0.cache) == 1

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    bounded_a_s_t_cache_0 = module_0.BoundedASTCache()
    assert f'{type(bounded_a_s_t_cache_0).__module__}.{type(bounded_a_s_t_cache_0).__qualname__}' == 'snippet_130.BoundedASTCache'
    assert f'{type(bounded_a_s_t_cache_0.cache).__module__}.{type(bounded_a_s_t_cache_0.cache).__qualname__}' == 'collections.OrderedDict'
    assert len(bounded_a_s_t_cache_0.cache) == 0
    assert bounded_a_s_t_cache_0.max_entries == 1000
    assert bounded_a_s_t_cache_0.max_memory_bytes == 524288000
    bounded_a_s_t_cache_0.__delitem__(bool_0)
    bounded_a_s_t_cache_0.__getitem__(bool_0)

def test_case_2():
    bounded_a_s_t_cache_0 = module_0.BoundedASTCache()
    assert f'{type(bounded_a_s_t_cache_0).__module__}.{type(bounded_a_s_t_cache_0).__qualname__}' == 'snippet_130.BoundedASTCache'
    assert f'{type(bounded_a_s_t_cache_0.cache).__module__}.{type(bounded_a_s_t_cache_0.cache).__qualname__}' == 'collections.OrderedDict'
    assert len(bounded_a_s_t_cache_0.cache) == 0
    assert bounded_a_s_t_cache_0.max_entries == 1000
    assert bounded_a_s_t_cache_0.max_memory_bytes == 524288000
    bool_0 = False
    bounded_a_s_t_cache_0.__delitem__(bool_0)
    bool_1 = bounded_a_s_t_cache_0.__contains__(bounded_a_s_t_cache_0)
    assert bool_1 is False
    bounded_a_s_t_cache_0.items()

def test_case_3():
    bounded_a_s_t_cache_0 = module_0.BoundedASTCache()
    assert f'{type(bounded_a_s_t_cache_0).__module__}.{type(bounded_a_s_t_cache_0).__qualname__}' == 'snippet_130.BoundedASTCache'
    assert f'{type(bounded_a_s_t_cache_0.cache).__module__}.{type(bounded_a_s_t_cache_0.cache).__qualname__}' == 'collections.OrderedDict'
    assert len(bounded_a_s_t_cache_0.cache) == 0
    assert bounded_a_s_t_cache_0.max_entries == 1000
    assert bounded_a_s_t_cache_0.max_memory_bytes == 524288000
    bounded_a_s_t_cache_0.items()