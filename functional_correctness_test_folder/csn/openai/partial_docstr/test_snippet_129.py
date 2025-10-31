import pytest
import snippet_129 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '|^m]\\F'
    set_0 = {str_0, str_0}
    fenwick_node_0 = module_0.FenwickNode(set_0, str_0)
    assert f'{type(fenwick_node_0).__module__}.{type(fenwick_node_0).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_0.children == '|^m]\\F'
    assert fenwick_node_0.parent == {'|^m]\\F'}
    assert fenwick_node_0.index is None
    assert module_0.FenwickNode.parent is None
    assert module_0.FenwickNode.children is None
    assert module_0.FenwickNode.index is None
    fenwick_node_0.get_ancestors()

def test_case_1():
    none_type_0 = None
    fenwick_node_0 = module_0.FenwickNode(none_type_0, none_type_0)
    assert f'{type(fenwick_node_0).__module__}.{type(fenwick_node_0).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_0.children is None
    assert fenwick_node_0.parent is None
    assert fenwick_node_0.index is None
    assert module_0.FenwickNode.parent is None
    assert module_0.FenwickNode.children is None
    assert module_0.FenwickNode.index is None
    fenwick_node_0.get_ancestors()

def test_case_2():
    none_type_0 = None
    fenwick_node_0 = module_0.FenwickNode(none_type_0, none_type_0)
    assert f'{type(fenwick_node_0).__module__}.{type(fenwick_node_0).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_0.children is None
    assert fenwick_node_0.parent is None
    assert fenwick_node_0.index is None
    assert module_0.FenwickNode.parent is None
    assert module_0.FenwickNode.children is None
    assert module_0.FenwickNode.index is None

@pytest.mark.xfail(strict=True)
def test_case_3():
    list_0 = []
    list_1 = [list_0, list_0, list_0]
    tuple_0 = (list_1,)
    none_type_0 = None
    fenwick_node_0 = module_0.FenwickNode(tuple_0, list_0, none_type_0)
    assert f'{type(fenwick_node_0).__module__}.{type(fenwick_node_0).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_0.children == []
    assert fenwick_node_0.parent == ([[], [], []],)
    assert fenwick_node_0.index is None
    assert module_0.FenwickNode.parent is None
    assert module_0.FenwickNode.children is None
    assert module_0.FenwickNode.index is None
    fenwick_node_1 = module_0.FenwickNode(fenwick_node_0, list_0)
    assert f'{type(fenwick_node_1).__module__}.{type(fenwick_node_1).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_1.children == []
    assert f'{type(fenwick_node_1.parent).__module__}.{type(fenwick_node_1.parent).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_1.index is None
    fenwick_node_1.get_ancestors()

def test_case_4():
    none_type_0 = None
    fenwick_node_0 = module_0.FenwickNode(none_type_0, none_type_0)
    assert f'{type(fenwick_node_0).__module__}.{type(fenwick_node_0).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_0.children is None
    assert fenwick_node_0.parent is None
    assert fenwick_node_0.index is None
    assert module_0.FenwickNode.parent is None
    assert module_0.FenwickNode.children is None
    assert module_0.FenwickNode.index is None
    fenwick_node_1 = module_0.FenwickNode(fenwick_node_0, fenwick_node_0, none_type_0)
    assert f'{type(fenwick_node_1).__module__}.{type(fenwick_node_1).__qualname__}' == 'snippet_129.FenwickNode'
    assert f'{type(fenwick_node_1.children).__module__}.{type(fenwick_node_1.children).__qualname__}' == 'snippet_129.FenwickNode'
    assert f'{type(fenwick_node_1.parent).__module__}.{type(fenwick_node_1.parent).__qualname__}' == 'snippet_129.FenwickNode'
    assert fenwick_node_1.index is None
    fenwick_node_1.get_ancestors()