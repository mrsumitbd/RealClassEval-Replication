import pytest
import snippet_107 as module_0

def test_case_0():
    bool_0 = False
    str_0 = 'd%M@`Y8X35'
    context_0 = module_0.Context(str_0, bool_0, bool_0, bool_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 10
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'
    str_1 = context_0.__repr__()
    assert str_1 == "Context(text='d%M@`Y8X35', token_count=False, start_index=False, end_index=False)"

@pytest.mark.xfail(strict=True)
def test_case_1():
    list_0 = []
    str_0 = '!CrxTp%/#*!.w@_'
    int_0 = 687
    context_0 = module_0.Context(str_0, int_0, int_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 15
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'
    context_0.to_dict()
    str_1 = context_0.__repr__()
    assert str_1 == "Context(text='!CrxTp%/#*!.w@_', token_count=687, start_index=687, end_index=None)"
    str_2 = context_0.__str__()
    assert str_2 == '!CrxTp%/#*!.w@_'
    int_1 = context_0.__len__()
    assert int_1 == 15
    module_0.Context(int_0, context_0, list_0, int_1)

def test_case_2():
    bool_0 = False
    str_0 = 'd%M@`Y8X35'
    context_0 = module_0.Context(str_0, bool_0, bool_0, bool_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 10
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'
    context_0.to_dict()
    str_1 = context_0.__str__()
    assert str_1 == 'd%M@`Y8X35'

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = '51\x0bR5'
    str_1 = 'ENrys@`O'
    none_type_0 = None
    context_0 = module_0.Context(str_1, none_type_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 8
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'
    int_0 = -3972
    module_0.Context(str_0, str_0, end_index=int_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = 'n#d\r'
    int_0 = -3972
    module_0.Context(str_0, int_0)

def test_case_5():
    int_0 = 1354
    str_0 = 'oFd#md6U\x0c\rQ=@p+]k'
    none_type_0 = None
    context_0 = module_0.Context(str_0, int_0, none_type_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 17
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'

def test_case_6():
    str_0 = '!CrxTp%/#*!.w@_'
    int_0 = 679
    context_0 = module_0.Context(str_0, int_0, int_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 15
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'

@pytest.mark.xfail(strict=True)
def test_case_7():
    bool_0 = False
    none_type_0 = None
    str_0 = 'p*hH=9\x0cw5;v q'
    int_0 = 399
    module_0.Context(str_0, none_type_0, int_0, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    bool_0 = False
    str_0 = 'd%M@`Y8X35'
    int_0 = -1866
    module_0.Context(str_0, bool_0, end_index=int_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    bool_0 = False
    str_0 = 'd%M@`Y8X35'
    context_0 = module_0.Context(str_0, bool_0, bool_0, bool_0)
    assert f'{type(context_0).__module__}.{type(context_0).__qualname__}' == 'snippet_107.Context'
    assert len(context_0) == 10
    assert module_0.Context.start_index is None
    assert module_0.Context.end_index is None
    assert f'{type(module_0.Context.from_dict).__module__}.{type(module_0.Context.from_dict).__qualname__}' == 'builtins.method'
    context_0.to_dict()
    int_0 = -3208
    str_1 = context_0.__repr__()
    assert str_1 == "Context(text='d%M@`Y8X35', token_count=False, start_index=False, end_index=False)"
    int_1 = context_0.__len__()
    assert int_1 == 10
    str_2 = 'c%vNT\t.|@QP*Yf\rrB&'
    none_type_0 = None
    module_0.Context(str_2, none_type_0, int_0, bool_0)