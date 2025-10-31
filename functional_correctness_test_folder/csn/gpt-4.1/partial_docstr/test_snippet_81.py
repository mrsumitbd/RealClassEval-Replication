import pytest
import snippet_81 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    ch_dir_0 = module_0.ChDir(bool_0)
    assert f'{type(ch_dir_0).__module__}.{type(ch_dir_0).__qualname__}' == 'snippet_81.ChDir'
    ch_dir_0.__enter__()

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    ch_dir_0 = module_0.ChDir(none_type_0)
    assert f'{type(ch_dir_0).__module__}.{type(ch_dir_0).__qualname__}' == 'snippet_81.ChDir'
    var_0 = ch_dir_0.__enter__()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_81.ChDir'
    none_type_1 = None
    bool_0 = True
    ch_dir_1 = module_0.ChDir(bool_0)
    assert f'{type(ch_dir_1).__module__}.{type(ch_dir_1).__qualname__}' == 'snippet_81.ChDir'
    ch_dir_1.__exit__(none_type_1, none_type_1, none_type_1)

@pytest.mark.xfail(strict=True)
def test_case_2():
    bool_0 = False
    ch_dir_0 = module_0.ChDir(bool_0)
    assert f'{type(ch_dir_0).__module__}.{type(ch_dir_0).__qualname__}' == 'snippet_81.ChDir'
    set_0 = set()
    ch_dir_1 = module_0.ChDir(set_0)
    assert f'{type(ch_dir_1).__module__}.{type(ch_dir_1).__qualname__}' == 'snippet_81.ChDir'
    ch_dir_1.__exit__(ch_dir_0, ch_dir_0, bool_0)

def test_case_3():
    none_type_0 = None
    ch_dir_0 = module_0.ChDir(none_type_0)
    assert f'{type(ch_dir_0).__module__}.{type(ch_dir_0).__qualname__}' == 'snippet_81.ChDir'
    ch_dir_0.__exit__(none_type_0, none_type_0, none_type_0)

def test_case_4():
    bool_0 = True
    ch_dir_0 = module_0.ChDir(bool_0)
    assert f'{type(ch_dir_0).__module__}.{type(ch_dir_0).__qualname__}' == 'snippet_81.ChDir'