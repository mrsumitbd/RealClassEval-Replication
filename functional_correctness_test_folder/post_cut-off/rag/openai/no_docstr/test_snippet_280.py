import pytest
import snippet_280 as module_0

def test_case_0():
    bool_0 = False
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    bound_worker_method_0 = module_0.BoundWorkerMethod(dict_0, bool_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    bound_worker_method_0 = module_0.BoundWorkerMethod(none_type_0, none_type_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    bound_worker_method_0.__call__()

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = '8L}njlsnOa`'
    float_0 = -916.29
    none_type_0 = None
    bound_worker_method_0 = module_0.BoundWorkerMethod(none_type_0, none_type_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    str_1 = '9('
    str_2 = '=hK+z9/ xV\x0bI1F?hIgk'
    dict_0 = {str_1: float_0, str_0: none_type_0, str_2: str_2}
    bound_worker_method_0.submit(**dict_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    str_0 = '1(xop,nZV.9hzl`'
    bound_worker_method_0 = module_0.BoundWorkerMethod(none_type_0, none_type_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    str_1 = "c\x0beF{Y4g'en6\x0c{r"
    dict_0 = {str_1: str_0, str_1: str_1}
    bound_worker_method_0.run_and_wait(**dict_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    none_type_0 = None
    bound_worker_method_0 = module_0.BoundWorkerMethod(none_type_0, none_type_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    bound_worker_method_0.set_pool(bound_worker_method_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    list_0 = []
    str_0 = '#30am8xna\x0b!!zJApb M'
    str_1 = '5M~$3}\x0bzb5'
    dict_0 = {str_0: list_0, str_0: str_0, str_1: str_1}
    bound_worker_method_0 = module_0.BoundWorkerMethod(dict_0, dict_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    bound_worker_method_0.shutdown_default_pool()

@pytest.mark.xfail(strict=True)
def test_case_6():
    int_0 = -138
    list_0 = [int_0, int_0]
    complex_0 = -518.3 + 2964.27j
    none_type_0 = None
    bound_worker_method_0 = module_0.BoundWorkerMethod(complex_0, none_type_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    bound_worker_method_1 = module_0.BoundWorkerMethod(bound_worker_method_0, none_type_0)
    assert f'{type(bound_worker_method_1).__module__}.{type(bound_worker_method_1).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    bound_worker_method_1.__getattr__(list_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    none_type_0 = None
    bool_0 = False
    bound_worker_method_0 = module_0.BoundWorkerMethod(none_type_0, bool_0)
    assert f'{type(bound_worker_method_0).__module__}.{type(bound_worker_method_0).__qualname__}' == 'snippet_280.BoundWorkerMethod'
    bound_worker_method_0.async_call()