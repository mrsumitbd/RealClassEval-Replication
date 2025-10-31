import pytest
import snippet_33 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    data_manager_0 = module_0.DataManager()
    assert f'{type(data_manager_0).__module__}.{type(data_manager_0).__qualname__}' == 'snippet_33.DataManager'
    assert data_manager_0.cache_ttl == 30
    assert data_manager_0.hours_back == 192
    assert data_manager_0.data_path is None
    assert f'{type(module_0.DataManager.cache_age).__module__}.{type(module_0.DataManager.cache_age).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_error).__module__}.{type(module_0.DataManager.last_error).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_successful_fetch_time).__module__}.{type(module_0.DataManager.last_successful_fetch_time).__qualname__}' == 'builtins.property'
    data_manager_0.get_data(data_manager_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    data_manager_0 = module_0.DataManager()
    assert f'{type(data_manager_0).__module__}.{type(data_manager_0).__qualname__}' == 'snippet_33.DataManager'
    assert data_manager_0.cache_ttl == 30
    assert data_manager_0.hours_back == 192
    assert data_manager_0.data_path is None
    assert f'{type(module_0.DataManager.cache_age).__module__}.{type(module_0.DataManager.cache_age).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_error).__module__}.{type(module_0.DataManager.last_error).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_successful_fetch_time).__module__}.{type(module_0.DataManager.last_successful_fetch_time).__qualname__}' == 'builtins.property'
    data_manager_0.get_data()

def test_case_2():
    data_manager_0 = module_0.DataManager()
    assert f'{type(data_manager_0).__module__}.{type(data_manager_0).__qualname__}' == 'snippet_33.DataManager'
    assert data_manager_0.cache_ttl == 30
    assert data_manager_0.hours_back == 192
    assert data_manager_0.data_path is None
    assert f'{type(module_0.DataManager.cache_age).__module__}.{type(module_0.DataManager.cache_age).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_error).__module__}.{type(module_0.DataManager.last_error).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_successful_fetch_time).__module__}.{type(module_0.DataManager.last_successful_fetch_time).__qualname__}' == 'builtins.property'

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = '8M,dQbn'
    data_manager_0 = module_0.DataManager(hours_back=str_0, data_path=str_0)
    assert f'{type(data_manager_0).__module__}.{type(data_manager_0).__qualname__}' == 'snippet_33.DataManager'
    assert data_manager_0.cache_ttl == 30
    assert data_manager_0.hours_back == '8M,dQbn'
    assert data_manager_0.data_path == '8M,dQbn'
    assert f'{type(module_0.DataManager.cache_age).__module__}.{type(module_0.DataManager.cache_age).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_error).__module__}.{type(module_0.DataManager.last_error).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.DataManager.last_successful_fetch_time).__module__}.{type(module_0.DataManager.last_successful_fetch_time).__qualname__}' == 'builtins.property'
    data_manager_0.invalidate_cache()