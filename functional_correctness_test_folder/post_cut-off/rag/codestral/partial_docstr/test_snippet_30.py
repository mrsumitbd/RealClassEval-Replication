import pytest
import builtins as module_0
import dataclasses as module_1
import snippet_30 as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    none_type_1 = None
    bool_0 = False
    dict_0 = {}
    list_0 = [dict_0]
    bool_1 = True
    tuple_0 = (dict_0, list_0, bool_1)
    object_0 = module_0.object()
    int_0 = 981
    bytes_0 = b'\x03S\xa4#X!(\x06N\xcd8'
    var_0 = module_1.dataclass(order=int_0, unsafe_hash=bytes_0)
    assert f'{type(module_1.MISSING).__module__}.{type(module_1.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_1.KW_ONLY).__module__}.{type(module_1.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    var_1 = var_0.__eq__(object_0)
    var_2 = var_1.__repr__()
    assert var_2 == 'NotImplemented'
    var_3 = var_2.__eq__(tuple_0)
    var_4 = var_3.__eq__(bool_0)
    var_5 = var_4.__eq__(none_type_1)
    var_6 = var_5.__eq__(none_type_0)
    var_7 = var_6.__repr__()
    assert var_7 == 'NotImplemented'
    bool_2 = True
    none_type_2 = None
    aggregated_stats_0 = module_2.AggregatedStats(bool_2, cache_creation_tokens=none_type_2, cache_read_tokens=none_type_2)
    assert f'{type(aggregated_stats_0).__module__}.{type(aggregated_stats_0).__qualname__}' == 'snippet_30.AggregatedStats'
    assert aggregated_stats_0.input_tokens is True
    assert aggregated_stats_0.output_tokens == 0
    assert aggregated_stats_0.cache_creation_tokens is None
    assert aggregated_stats_0.cache_read_tokens is None
    assert aggregated_stats_0.cost == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert aggregated_stats_0.count == 0
    assert module_2.AggregatedStats.input_tokens == 0
    assert module_2.AggregatedStats.output_tokens == 0
    assert module_2.AggregatedStats.cache_creation_tokens == 0
    assert module_2.AggregatedStats.cache_read_tokens == 0
    assert module_2.AggregatedStats.cost == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_2.AggregatedStats.count == 0
    aggregated_stats_0.add_entry(var_7)

def test_case_1():
    bool_0 = True
    aggregated_stats_0 = module_2.AggregatedStats(output_tokens=bool_0, count=bool_0)
    assert f'{type(aggregated_stats_0).__module__}.{type(aggregated_stats_0).__qualname__}' == 'snippet_30.AggregatedStats'
    assert aggregated_stats_0.input_tokens == 0
    assert aggregated_stats_0.output_tokens is True
    assert aggregated_stats_0.cache_creation_tokens == 0
    assert aggregated_stats_0.cache_read_tokens == 0
    assert aggregated_stats_0.cost == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert aggregated_stats_0.count is True
    assert module_2.AggregatedStats.input_tokens == 0
    assert module_2.AggregatedStats.output_tokens == 0
    assert module_2.AggregatedStats.cache_creation_tokens == 0
    assert module_2.AggregatedStats.cache_read_tokens == 0
    assert module_2.AggregatedStats.cost == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_2.AggregatedStats.count == 0
    aggregated_stats_0.to_dict()