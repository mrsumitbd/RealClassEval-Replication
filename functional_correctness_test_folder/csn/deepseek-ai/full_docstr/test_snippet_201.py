import pytest
import snippet_201 as module_0
import inspect as module_1
import platform as module_2

def test_case_0():
    none_type_0 = None
    module_0.DigitalFilter(none_type_0, none_type_0)

def test_case_1():
    var_0 = module_1.currentframe()
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
    module_0.DigitalFilter(var_0, var_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    digital_filter_0 = module_0.DigitalFilter(none_type_0)
    module_0.DigitalFilter(digital_filter_0, filter_coeff=digital_filter_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    var_0 = module_2.release()
    digital_filter_0 = module_0.DigitalFilter(var_0)
    digital_filter_0.tofile()

@pytest.mark.xfail(strict=True)
def test_case_4():
    var_0 = module_2.release()
    digital_filter_0 = module_0.DigitalFilter(var_0)
    digital_filter_0.fromfile()