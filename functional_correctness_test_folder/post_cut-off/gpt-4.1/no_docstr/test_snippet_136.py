import dataclasses as module_0
import snippet_136 as module_1

def test_case_0():
    none_type_0 = None
    int_0 = -11
    str_0 = '](l`'
    str_1 = "Zc\x0beF{Y4g'en6\x0c{r]7"
    var_0 = module_0.dataclass(unsafe_hash=str_1, frozen=str_1)
    assert f'{type(module_0.MISSING).__module__}.{type(module_0.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_0.KW_ONLY).__module__}.{type(module_0.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    var_1 = var_0.__eq__(str_0)
    var_2 = var_1.__repr__()
    assert var_2 == 'NotImplemented'
    var_3 = var_2.__eq__(int_0)
    var_4 = var_3.__eq__(none_type_0)
    var_5 = var_4.__repr__()
    assert var_5 == 'NotImplemented'
    metric_result_0 = module_1.MetricResult(var_5, var_1, var_1)
    assert f'{type(metric_result_0).__module__}.{type(metric_result_0).__qualname__}' == 'snippet_136.MetricResult'
    assert metric_result_0.name == 'NotImplemented'
    assert f'{type(metric_result_0.params).__module__}.{type(metric_result_0.params).__qualname__}' == 'builtins.NotImplementedType'
    assert f'{type(metric_result_0.result).__module__}.{type(metric_result_0.result).__qualname__}' == 'builtins.NotImplementedType'
    assert f'{type(module_1.MetricResult.from_results_dict).__module__}.{type(module_1.MetricResult.from_results_dict).__qualname__}' == 'builtins.method'
    str_2 = metric_result_0.__str__()
    assert str_2 == 'NotImplemented: NotImplemented'