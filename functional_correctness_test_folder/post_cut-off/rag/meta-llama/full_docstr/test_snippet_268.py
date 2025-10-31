import pytest
import snippet_268 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = True
    dict_0 = {bool_0: bool_0, bool_0: bool_0, bool_0: bool_0}
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    index_manager_0.reindex(dict_0, index_manager_0)

def test_case_1():
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    none_type_0 = None
    index_manager_0.query(none_type_0, index_manager_0)

def test_case_2():
    str_0 = "Tow'KBs\tcZs,(\x0b"
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    index_manager_0.query_in(str_0, str_0)

def test_case_3():
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    none_type_0 = None
    var_0 = index_manager_0.query(none_type_0, index_manager_0)
    index_manager_0.query_in(index_manager_0, var_0)

def test_case_4():
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}

@pytest.mark.xfail(strict=True)
def test_case_5():
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    none_type_0 = None
    index_manager_0.query(none_type_0, index_manager_0)
    index_manager_0.reindex(index_manager_0, index_manager_0)

def test_case_6():
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    none_type_0 = None
    index_manager_0.query(index_manager_0, none_type_0)
    index_manager_0.clear()

@pytest.mark.xfail(strict=True)
def test_case_7():
    bool_0 = True
    bytes_0 = b'\xf8\xfd\xbcr\xa19\xd4'
    dict_0 = {bool_0: bytes_0, bytes_0: bytes_0, bytes_0: bytes_0}
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    index_manager_0.index(dict_0)
    none_type_0 = None
    index_manager_1 = module_0.IndexManager()
    assert f'{type(index_manager_1).__module__}.{type(index_manager_1).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_1.indexes).__module__}.{type(index_manager_1.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_1.indexes) == 0
    assert index_manager_1.doc_map == {}
    index_manager_1.reindex(none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    bool_0 = False
    dict_0 = {bool_0: bool_0, bool_0: bool_0, bool_0: bool_0}
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    var_0 = index_manager_0.index(dict_0)
    assert len(index_manager_0.indexes) == 1
    var_1 = index_manager_0.remove(dict_0)
    assert index_manager_0.doc_map == {}
    index_manager_0.query_in(dict_0, dict_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    bool_0 = False
    dict_0 = {bool_0: bool_0}
    none_type_0 = None
    index_manager_0 = module_0.IndexManager()
    assert f'{type(index_manager_0).__module__}.{type(index_manager_0).__qualname__}' == 'snippet_268.IndexManager'
    assert f'{type(index_manager_0.indexes).__module__}.{type(index_manager_0.indexes).__qualname__}' == 'collections.defaultdict'
    assert len(index_manager_0.indexes) == 0
    assert index_manager_0.doc_map == {}
    var_0 = index_manager_0.index(dict_0)
    assert len(index_manager_0.indexes) == 1
    var_1 = index_manager_0.remove(dict_0)
    assert index_manager_0.doc_map == {}
    index_manager_0.query(none_type_0, index_manager_0)
    index_manager_0.reindex(dict_0, bool_0)