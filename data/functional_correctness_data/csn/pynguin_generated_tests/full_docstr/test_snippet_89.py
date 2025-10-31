import pytest
import snippet_89 as module_0
import builtins as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'b5k@&zntj%pp~(Eo9\t'
    loader_0 = module_0.Loader(str_0, str_0)
    assert f'{type(loader_0).__module__}.{type(loader_0).__qualname__}' == 'snippet_89.Loader'
    assert f'{type(module_0.Loader.name).__module__}.{type(module_0.Loader.name).__qualname__}' == 'builtins.member_descriptor'
    loader_1 = module_0.Loader(str_0, str_0)
    assert f'{type(loader_1).__module__}.{type(loader_1).__qualname__}' == 'snippet_89.Loader'
    dict_0 = {loader_1: loader_0, loader_0: loader_0}
    loader_1.get_pipeline(loader_1, dict_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    loader_0 = module_0.Loader(none_type_0, none_type_0)
    assert f'{type(loader_0).__module__}.{type(loader_0).__qualname__}' == 'snippet_89.Loader'
    assert f'{type(module_0.Loader.name).__module__}.{type(module_0.Loader.name).__qualname__}' == 'builtins.member_descriptor'
    loader_0.get_pipeline(none_type_0, none_type_0)

def test_case_2():
    exception_0 = module_1.Exception()
    loader_0 = module_0.Loader(exception_0, exception_0)
    assert f'{type(loader_0).__module__}.{type(loader_0).__qualname__}' == 'snippet_89.Loader'
    assert f'{type(module_0.Loader.name).__module__}.{type(module_0.Loader.name).__qualname__}' == 'builtins.member_descriptor'

def test_case_3():
    str_0 = 'J$'
    loader_0 = module_0.Loader(str_0, str_0)
    assert f'{type(loader_0).__module__}.{type(loader_0).__qualname__}' == 'snippet_89.Loader'
    assert f'{type(module_0.Loader.name).__module__}.{type(module_0.Loader.name).__qualname__}' == 'builtins.member_descriptor'
    loader_0.clear()