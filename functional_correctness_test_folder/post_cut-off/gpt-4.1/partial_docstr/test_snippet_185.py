import pytest
import snippet_185 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = ':{g+4'
    int_0 = -3911
    top_k_string_tracker_0 = module_0.TopKStringTracker(int_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m == -3911
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    top_k_string_tracker_0.add_strings(str_0)

def test_case_1():
    str_0 = '}L:Q|[\x0cm9TT9$.\\0y*p'
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    none_type_0 = top_k_string_tracker_0.add_strings(str_0)
    assert len(top_k_string_tracker_0.count) == 17
    assert top_k_string_tracker_0.heap == [(2, '9')]
    assert top_k_string_tracker_0.in_heap == {'9'}

def test_case_2():
    int_0 = -2248
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    top_k_string_tracker_0.get_top_k(int_0)

def test_case_3():
    int_0 = -3328
    str_0 = '_y'
    set_0 = {str_0, str_0}
    top_k_string_tracker_0 = module_0.TopKStringTracker(set_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m == {'_y'}
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    top_k_string_tracker_0.get_top_k(int_0)
    bool_0 = True
    top_k_string_tracker_1 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_1).__module__}.{type(top_k_string_tracker_1).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_1.m is True
    assert f'{type(top_k_string_tracker_1.count).__module__}.{type(top_k_string_tracker_1.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_1.count) == 0
    assert top_k_string_tracker_1.heap == []
    assert top_k_string_tracker_1.in_heap == {*()}
    top_k_string_tracker_2 = module_0.TopKStringTracker(top_k_string_tracker_0)
    assert f'{type(top_k_string_tracker_2).__module__}.{type(top_k_string_tracker_2).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert f'{type(top_k_string_tracker_2.m).__module__}.{type(top_k_string_tracker_2.m).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert f'{type(top_k_string_tracker_2.count).__module__}.{type(top_k_string_tracker_2.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_2.count) == 0
    assert top_k_string_tracker_2.heap == []
    assert top_k_string_tracker_2.in_heap == {*()}
    int_1 = top_k_string_tracker_2.size()
    assert int_1 == 0
    int_2 = top_k_string_tracker_2.get_count(top_k_string_tracker_2)
    assert int_2 == 0
    top_k_string_tracker_1.trim_to_m()

def test_case_4():
    int_0 = 277
    top_k_string_tracker_0 = module_0.TopKStringTracker(int_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m == 277
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}

def test_case_5():
    str_0 = '}L:Q|[\x0cm9TT9$.\\0y*p'
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    int_0 = top_k_string_tracker_0.size()
    assert int_0 == 0
    none_type_0 = top_k_string_tracker_0.add_strings(str_0)
    assert len(top_k_string_tracker_0.count) == 17
    assert top_k_string_tracker_0.heap == [(2, '9')]
    assert top_k_string_tracker_0.in_heap == {'9'}

def test_case_6():
    str_0 = ':{g+4'
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    int_0 = top_k_string_tracker_0.size()
    assert int_0 == 0
    none_type_0 = top_k_string_tracker_0.add_strings(str_0)
    assert len(top_k_string_tracker_0.count) == 5
    assert top_k_string_tracker_0.heap == [(1, ':')]
    assert top_k_string_tracker_0.in_heap == {':'}
    none_type_1 = top_k_string_tracker_0.trim_to_m()
    assert len(top_k_string_tracker_0.count) == 1

def test_case_7():
    str_0 = ':{g+4'
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    int_0 = top_k_string_tracker_0.size()
    assert int_0 == 0
    none_type_0 = top_k_string_tracker_0.add_strings(str_0)
    assert len(top_k_string_tracker_0.count) == 5
    assert top_k_string_tracker_0.heap == [(1, ':')]
    assert top_k_string_tracker_0.in_heap == {':'}
    top_k_string_tracker_0.get_top_k(bool_0)

def test_case_8():
    str_0 = '}L:Q|[\x0cm9TT9$.\\0y*p'
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    int_0 = top_k_string_tracker_0.size()
    assert int_0 == 0
    none_type_0 = top_k_string_tracker_0.add_strings(str_0)
    assert len(top_k_string_tracker_0.count) == 17
    assert top_k_string_tracker_0.heap == [(2, '9')]
    assert top_k_string_tracker_0.in_heap == {'9'}
    none_type_1 = top_k_string_tracker_0.add_strings(str_0)
    assert top_k_string_tracker_0.heap == [(4, 'T')]
    assert top_k_string_tracker_0.in_heap == {'T'}

def test_case_9():
    bool_0 = True
    top_k_string_tracker_0 = module_0.TopKStringTracker(bool_0)
    assert f'{type(top_k_string_tracker_0).__module__}.{type(top_k_string_tracker_0).__qualname__}' == 'snippet_185.TopKStringTracker'
    assert top_k_string_tracker_0.m is True
    assert f'{type(top_k_string_tracker_0.count).__module__}.{type(top_k_string_tracker_0.count).__qualname__}' == 'collections.defaultdict'
    assert len(top_k_string_tracker_0.count) == 0
    assert top_k_string_tracker_0.heap == []
    assert top_k_string_tracker_0.in_heap == {*()}
    int_0 = top_k_string_tracker_0.size()
    assert int_0 == 0
    bool_1 = False
    top_k_string_tracker_0.get_top_k(bool_1)
    none_type_0 = None
    dict_0 = {none_type_0: int_0}
    top_k_string_tracker_0.add_string_dict(dict_0)