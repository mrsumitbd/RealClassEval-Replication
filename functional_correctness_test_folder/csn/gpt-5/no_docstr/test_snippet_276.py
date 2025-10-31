import pytest
import snippet_276 as module_0

def test_case_0():
    bool_0 = True
    dict_0 = {bool_0: bool_0, bool_0: bool_0, bool_0: bool_0}
    none_type_0 = None
    query_single_0 = module_0.QuerySingle(dict_0, none_type_0, query_params=dict_0)
    assert f'{type(query_single_0).__module__}.{type(query_single_0).__qualname__}' == 'snippet_276.QuerySingle'
    assert query_single_0.conn == {True: True}
    assert query_single_0.object_type is None
    assert query_single_0.url_params == []
    assert query_single_0.query_params == {True: True}
    query_single_0.reload()
    bool_1 = True
    set_0 = {bool_1, bool_1, bool_1}
    query_single_1 = module_0.QuerySingle(bool_1, set_0, set_0)
    assert f'{type(query_single_1).__module__}.{type(query_single_1).__qualname__}' == 'snippet_276.QuerySingle'
    assert query_single_1.conn is True
    assert query_single_1.object_type == {True}
    assert query_single_1.url_params == {True}
    assert query_single_1.query_params == {}

def test_case_1():
    bool_0 = True
    query_single_0 = module_0.QuerySingle(bool_0, bool_0)
    assert f'{type(query_single_0).__module__}.{type(query_single_0).__qualname__}' == 'snippet_276.QuerySingle'
    assert query_single_0.conn is True
    assert query_single_0.object_type is True
    assert query_single_0.url_params == []
    assert query_single_0.query_params == {}

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    query_single_0 = module_0.QuerySingle(none_type_0, none_type_0)
    assert f'{type(query_single_0).__module__}.{type(query_single_0).__qualname__}' == 'snippet_276.QuerySingle'
    assert query_single_0.conn is None
    assert query_single_0.object_type is None
    assert query_single_0.url_params == []
    assert query_single_0.query_params == {}
    query_single_0.result()

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    query_single_0 = module_0.QuerySingle(none_type_0, none_type_0, none_type_0)
    assert f'{type(query_single_0).__module__}.{type(query_single_0).__qualname__}' == 'snippet_276.QuerySingle'
    assert query_single_0.conn is None
    assert query_single_0.object_type is None
    assert query_single_0.url_params == []
    assert query_single_0.query_params == {}
    query_single_0.reload()
    query_single_0.result()