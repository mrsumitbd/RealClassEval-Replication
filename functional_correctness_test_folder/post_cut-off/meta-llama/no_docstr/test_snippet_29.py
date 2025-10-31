import pytest
import snippet_29 as module_0

def test_case_0():
    last_used_params_0 = module_0.LastUsedParams()
    assert f'{type(last_used_params_0).__module__}.{type(last_used_params_0).__qualname__}' == 'snippet_29.LastUsedParams'
    assert f'{type(last_used_params_0.config_dir).__module__}.{type(last_used_params_0.config_dir).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(last_used_params_0.params_file).__module__}.{type(last_used_params_0.params_file).__qualname__}' == 'pathlib.PosixPath'

@pytest.mark.xfail(strict=True)
def test_case_1():
    last_used_params_0 = module_0.LastUsedParams()
    assert f'{type(last_used_params_0).__module__}.{type(last_used_params_0).__qualname__}' == 'snippet_29.LastUsedParams'
    assert f'{type(last_used_params_0.config_dir).__module__}.{type(last_used_params_0.config_dir).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(last_used_params_0.params_file).__module__}.{type(last_used_params_0.params_file).__qualname__}' == 'pathlib.PosixPath'
    last_used_params_0.save(last_used_params_0)

def test_case_2():
    last_used_params_0 = module_0.LastUsedParams()
    assert f'{type(last_used_params_0).__module__}.{type(last_used_params_0).__qualname__}' == 'snippet_29.LastUsedParams'
    assert f'{type(last_used_params_0.config_dir).__module__}.{type(last_used_params_0.config_dir).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(last_used_params_0.params_file).__module__}.{type(last_used_params_0.params_file).__qualname__}' == 'pathlib.PosixPath'
    last_used_params_0.load()

@pytest.mark.xfail(strict=True)
def test_case_3():
    last_used_params_0 = module_0.LastUsedParams()
    assert f'{type(last_used_params_0).__module__}.{type(last_used_params_0).__qualname__}' == 'snippet_29.LastUsedParams'
    assert f'{type(last_used_params_0.config_dir).__module__}.{type(last_used_params_0.config_dir).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(last_used_params_0.params_file).__module__}.{type(last_used_params_0.params_file).__qualname__}' == 'pathlib.PosixPath'
    last_used_params_0.clear()
    last_used_params_0.load()
    module_0.LastUsedParams(last_used_params_0)

def test_case_4():
    last_used_params_0 = module_0.LastUsedParams()
    assert f'{type(last_used_params_0).__module__}.{type(last_used_params_0).__qualname__}' == 'snippet_29.LastUsedParams'
    assert f'{type(last_used_params_0.config_dir).__module__}.{type(last_used_params_0.config_dir).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(last_used_params_0.params_file).__module__}.{type(last_used_params_0.params_file).__qualname__}' == 'pathlib.PosixPath'
    last_used_params_0.clear()

def test_case_5():
    last_used_params_0 = module_0.LastUsedParams()
    assert f'{type(last_used_params_0).__module__}.{type(last_used_params_0).__qualname__}' == 'snippet_29.LastUsedParams'
    assert f'{type(last_used_params_0.config_dir).__module__}.{type(last_used_params_0.config_dir).__qualname__}' == 'pathlib.PosixPath'
    assert f'{type(last_used_params_0.params_file).__module__}.{type(last_used_params_0.params_file).__qualname__}' == 'pathlib.PosixPath'
    last_used_params_0.load()
    bool_0 = last_used_params_0.exists()
    assert bool_0 is False