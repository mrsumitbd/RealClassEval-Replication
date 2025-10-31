import pytest
import snippet_310 as module_0

def test_case_0():
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'

def test_case_1():
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = "H7/{~Q\nQ'"
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_1 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_1).__module__}.{type(in_memory_cache_1).__qualname__}' == 'snippet_310.InMemoryCache'
    var_0 = in_memory_cache_1.__new__(in_memory_cache_1)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_310.InMemoryCache'
    var_1 = var_0.__new__(in_memory_cache_1)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_0.get(var_0)
    var_0.set(var_1, str_0, in_memory_cache_1)

def test_case_3():
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    str_0 = '\nx#FA4{'
    in_memory_cache_1 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_1).__module__}.{type(in_memory_cache_1).__qualname__}' == 'snippet_310.InMemoryCache'
    none_type_0 = None
    in_memory_cache_1.set(str_0, none_type_0)
    in_memory_cache_0.get(str_0)

def test_case_4():
    str_0 = "H7/{~Q\nQ'"
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_0.get(str_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = '?AT;x$MKY!nN'
    list_0 = [str_0, str_0]
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_0.get(list_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    tuple_0 = ()
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_0.delete(tuple_0)
    list_0 = []
    in_memory_cache_1 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_1).__module__}.{type(in_memory_cache_1).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_1.delete(list_0)

def test_case_7():
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    none_type_0 = None
    in_memory_cache_0.delete(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    list_0 = []
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_0.delete(list_0)

def test_case_9():
    int_0 = -998
    str_0 = "H7/{~Q\nQ'"
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    var_0 = in_memory_cache_0.get(str_0)
    var_1 = in_memory_cache_0.__new__(in_memory_cache_0)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_0.set(var_0, int_0, int_0)
    var_1.set(var_0, str_0, var_0)

@pytest.mark.xfail(strict=True)
def test_case_10():
    tuple_0 = ()
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    bool_0 = False
    in_memory_cache_1 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_1).__module__}.{type(in_memory_cache_1).__qualname__}' == 'snippet_310.InMemoryCache'
    in_memory_cache_1.set(tuple_0, tuple_0, bool_0)
    none_type_0 = in_memory_cache_0.delete(tuple_0)
    str_0 = '@T\r'
    in_memory_cache_0.set(str_0, tuple_0)
    list_0 = []
    in_memory_cache_2 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_2).__module__}.{type(in_memory_cache_2).__qualname__}' == 'snippet_310.InMemoryCache'
    str_1 = 'PjR'
    var_0 = in_memory_cache_2.get(str_1, none_type_0)
    assert var_0 is True
    in_memory_cache_0.delete(list_0)

def test_case_11():
    str_0 = "H7/{~Q\nQ'"
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    var_0 = in_memory_cache_0.get(str_0)
    in_memory_cache_1 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_1).__module__}.{type(in_memory_cache_1).__qualname__}' == 'snippet_310.InMemoryCache'
    var_1 = in_memory_cache_1.__new__(in_memory_cache_1)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_310.InMemoryCache'
    var_2 = in_memory_cache_0.get(var_1)
    assert var_2 == "H7/{~Q\nQ'"
    in_memory_cache_1.delete(in_memory_cache_0)
    none_type_0 = in_memory_cache_1.delete(var_2)
    in_memory_cache_0.set(var_0, none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_12():
    str_0 = "H7/{~Q\nQ'"
    in_memory_cache_0 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_0).__module__}.{type(in_memory_cache_0).__qualname__}' == 'snippet_310.InMemoryCache'
    var_0 = in_memory_cache_0.get(str_0)
    in_memory_cache_1 = module_0.InMemoryCache()
    assert f'{type(in_memory_cache_1).__module__}.{type(in_memory_cache_1).__qualname__}' == 'snippet_310.InMemoryCache'
    var_1 = in_memory_cache_1.__new__(in_memory_cache_1)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_310.InMemoryCache'
    var_2 = in_memory_cache_0.get(var_1)
    in_memory_cache_1.delete(var_2)
    var_1.set(var_0, str_0, in_memory_cache_1)