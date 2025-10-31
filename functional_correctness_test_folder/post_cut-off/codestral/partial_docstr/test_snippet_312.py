import pytest
import snippet_312 as module_0

def test_case_0():
    dict_0 = {}
    str_0 = ']NOFY9p+g|v\x0b*&?I'
    notes_search_controller_0 = module_0.NotesSearchController()
    assert f'{type(notes_search_controller_0).__module__}.{type(notes_search_controller_0).__qualname__}' == 'snippet_312.NotesSearchController'
    notes_search_controller_0.search_notes(dict_0, str_0)

def test_case_1():
    str_0 = '/rnGxMZQLeJ=\n4'
    dict_0 = {}
    list_0 = [dict_0, dict_0]
    notes_search_controller_0 = module_0.NotesSearchController()
    assert f'{type(notes_search_controller_0).__module__}.{type(notes_search_controller_0).__qualname__}' == 'snippet_312.NotesSearchController'
    notes_search_controller_0.search_notes(list_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = ')dDGIdj7DZY+'
    notes_search_controller_0 = module_0.NotesSearchController()
    assert f'{type(notes_search_controller_0).__module__}.{type(notes_search_controller_0).__qualname__}' == 'snippet_312.NotesSearchController'
    notes_search_controller_0.search_notes(str_0, str_0)

def test_case_3():
    notes_search_controller_0 = module_0.NotesSearchController()
    assert f'{type(notes_search_controller_0).__module__}.{type(notes_search_controller_0).__qualname__}' == 'snippet_312.NotesSearchController'
    list_0 = []
    str_0 = ''
    notes_search_controller_0.search_notes(list_0, str_0)