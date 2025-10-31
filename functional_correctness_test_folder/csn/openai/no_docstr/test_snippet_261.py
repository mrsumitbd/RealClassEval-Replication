import pytest
import snippet_261 as module_0
import numexpr.utils as module_1
import pyarrow.compute as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    import__data_0 = module_0.Import_Data()
    import__data_0.import_csv()

def test_case_1():
    import__data_0 = module_0.Import_Data()
    none_type_0 = None
    with pytest.raises(NotImplementedError):
        import__data_0.import_csv(import__data_0, convert_col=import__data_0, concat_files=none_type_0)

def test_case_2():
    module_0.Import_Data()

def test_case_3():
    import__data_0 = module_0.Import_Data()
    with pytest.raises(NotImplementedError):
        import__data_0.import_csv(folder_name=import__data_0, index_col=import__data_0)

def test_case_4():
    import__data_0 = module_0.Import_Data()
    list_0 = []
    import__data_0.import_csv(list_0, index_col=list_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    var_0 = module_1.get_vml_num_threads()
    assert f'{type(module_1.log).__module__}.{type(module_1.log).__qualname__}' == 'logging.Logger'
    assert module_1.log.filters == []
    assert module_1.log.name == 'numexpr.utils'
    assert module_1.log.level == 0
    assert f'{type(module_1.log.parent).__module__}.{type(module_1.log.parent).__qualname__}' == 'logging.RootLogger'
    assert module_1.log.propagate is True
    assert module_1.log.handlers == []
    assert module_1.log.disabled is False
    assert f'{type(module_1.log.manager).__module__}.{type(module_1.log.manager).__qualname__}' == 'logging.Manager'
    assert module_1.use_vml is False
    assert module_1.MAX_THREADS == 64
    var_1 = module_2.acos(var_0)
    var_2 = var_1.__str__()
    import__data_0 = module_0.Import_Data()
    import__data_0.import_csv(var_2, head_row=var_2)

@pytest.mark.xfail(strict=True)
def test_case_6():
    import__data_0 = module_0.Import_Data()
    var_0 = import__data_0.__str__()
    import__data_0.import_csv(folder_name=var_0, convert_col=var_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    var_0 = module_1.get_vml_num_threads()
    assert f'{type(module_1.log).__module__}.{type(module_1.log).__qualname__}' == 'logging.Logger'
    assert module_1.log.filters == []
    assert module_1.log.name == 'numexpr.utils'
    assert module_1.log.level == 0
    assert f'{type(module_1.log.parent).__module__}.{type(module_1.log.parent).__qualname__}' == 'logging.RootLogger'
    assert module_1.log.propagate is True
    assert module_1.log.handlers == []
    assert module_1.log.disabled is False
    assert f'{type(module_1.log.manager).__module__}.{type(module_1.log.manager).__qualname__}' == 'logging.Manager'
    assert module_1.use_vml is False
    assert module_1.MAX_THREADS == 64
    var_1 = module_2.acos(var_0)
    var_2 = var_1.__str__()
    import__data_0 = module_0.Import_Data()
    import__data_0.import_csv(var_2, var_2)

@pytest.mark.xfail(strict=True)
def test_case_8():
    import__data_0 = module_0.Import_Data()
    var_0 = import__data_0.__str__()
    import__data_0.import_csv(var_0)