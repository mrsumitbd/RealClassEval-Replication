import pytest
import snippet_75 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'Ab\\5sESDHV%/&0~'
    module_0.GoogleCustomSearchAPI(str_0, str_0, str_0, str_0)

def test_case_1():
    none_type_0 = None
    bool_0 = False
    google_custom_search_a_p_i_0 = module_0.GoogleCustomSearchAPI(none_type_0, none_type_0, bool_0, bool_0)
    google_custom_search_a_p_i_0.get_all_results(none_type_0)

def test_case_2():
    none_type_0 = None
    bool_0 = False
    google_custom_search_a_p_i_0 = module_0.GoogleCustomSearchAPI(none_type_0, none_type_0, bool_0, bool_0)
    google_custom_search_a_p_i_0.get_all_results(google_custom_search_a_p_i_0, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'C2wkj'
    none_type_0 = None
    bool_0 = False
    google_custom_search_a_p_i_0 = module_0.GoogleCustomSearchAPI(none_type_0, none_type_0, bool_0, bool_0)
    google_custom_search_a_p_i_0.get_all_results(none_type_0)
    google_custom_search_a_p_i_0.search(bool_0, str_0)