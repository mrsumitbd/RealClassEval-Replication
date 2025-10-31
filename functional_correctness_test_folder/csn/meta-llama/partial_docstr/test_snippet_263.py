import pytest
import snippet_263 as module_0
import inspect as module_1
import platform as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    import__data_0 = module_0.Import_Data()
    import__data_0.import_csv()

def test_case_1():
    import__data_0 = module_0.Import_Data()
    with pytest.raises(NotImplementedError):
        import__data_0.import_csv(import__data_0, head_row=import__data_0)

def test_case_2():
    module_0.Import_Data()

def test_case_3():
    import__data_0 = module_0.Import_Data()
    with pytest.raises(NotImplementedError):
        import__data_0.import_csv(folder_name=import__data_0, concat_files=import__data_0)

def test_case_4():
    import__data_0 = module_0.Import_Data()
    none_type_0 = None
    var_0 = module_1.trace()
    assert f'{type(module_1.mod_dict).__module__}.{type(module_1.mod_dict).__qualname__}' == 'builtins.dict'
    assert len(module_1.mod_dict) == 168
    assert module_1.k == 512
    assert module_1.v == 'ASYNC_GENERATOR'
    assert module_1.CO_OPTIMIZED == 1
    assert module_1.CO_NEWLOCALS == 2
    assert module_1.CO_VARARGS == 4
    assert module_1.CO_VARKEYWORDS == 8
    assert module_1.CO_NESTED == 16
    assert module_1.CO_GENERATOR == 32
    assert module_1.CO_NOFREE == 64
    assert module_1.CO_COROUTINE == 128
    assert module_1.CO_ITERABLE_COROUTINE == 256
    assert module_1.CO_ASYNC_GENERATOR == 512
    assert module_1.TPFLAGS_IS_ABSTRACT == 1048576
    assert module_1.modulesbyfile == {}
    assert module_1.GEN_CREATED == 'GEN_CREATED'
    assert module_1.GEN_RUNNING == 'GEN_RUNNING'
    assert module_1.GEN_SUSPENDED == 'GEN_SUSPENDED'
    assert module_1.GEN_CLOSED == 'GEN_CLOSED'
    assert module_1.CORO_CREATED == 'CORO_CREATED'
    assert module_1.CORO_RUNNING == 'CORO_RUNNING'
    assert module_1.CORO_SUSPENDED == 'CORO_SUSPENDED'
    assert module_1.CORO_CLOSED == 'CORO_CLOSED'
    import__data_0.import_csv(var_0, head_row=import__data_0, index_col=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    import__data_0 = module_0.Import_Data()
    var_0 = module_2.python_branch()
    import__data_0.import_csv(var_0, head_row=import__data_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    import__data_0 = module_0.Import_Data()
    str_0 = 'IdJOz?rc9y'
    import__data_0.import_csv(folder_name=str_0, index_col=import__data_0, convert_col=import__data_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    import__data_0 = module_0.Import_Data()
    var_0 = module_2.python_branch()
    import__data_0.import_csv(var_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    import__data_0 = module_0.Import_Data()
    import__data_1 = module_0.Import_Data()
    var_0 = module_2.python_branch()
    import__data_0.import_csv(var_0, var_0, import__data_1, var_0)