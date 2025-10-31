import pytest
import snippet_55 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    module_0.Exporter(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    dict_0 = {}
    exporter_0 = module_0.Exporter(dict_0)
    assert f'{type(exporter_0).__module__}.{type(exporter_0).__qualname__}' == 'snippet_55.Exporter'
    assert exporter_0.globls == {'__all__': []}
    assert exporter_0.exports == []
    exporter_0.export(none_type_0)

def test_case_2():
    str_0 = '&NJ)BsXM"\roVh'
    str_1 = '_\x0bfIEI^l}3^N+j5'
    dict_0 = {str_0: str_0, str_1: str_0, str_1: str_1}
    exporter_0 = module_0.Exporter(dict_0)
    assert f'{type(exporter_0).__module__}.{type(exporter_0).__qualname__}' == 'snippet_55.Exporter'
    assert exporter_0.globls == {'&NJ)BsXM"\roVh': '&NJ)BsXM"\roVh', '_\x0bfIEI^l}3^N+j5': '_\x0bfIEI^l}3^N+j5', '__all__': []}
    assert exporter_0.exports == []
    var_0 = exporter_0.__enter__()
    assert exporter_0.start_vars == {'&NJ)BsXM"\roVh', '_\x0bfIEI^l}3^N+j5', '__all__'}

@pytest.mark.xfail(strict=True)
def test_case_3():
    int_0 = -1936
    none_type_0 = None
    bool_0 = False
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    exporter_0 = module_0.Exporter(dict_0)
    assert f'{type(exporter_0).__module__}.{type(exporter_0).__qualname__}' == 'snippet_55.Exporter'
    assert exporter_0.globls == {False: False, '__all__': []}
    assert exporter_0.exports == []
    exporter_0.__exit__(int_0, none_type_0, none_type_0)