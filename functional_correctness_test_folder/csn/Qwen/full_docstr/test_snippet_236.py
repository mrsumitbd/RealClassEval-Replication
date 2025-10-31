import pytest
import snippet_236 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    search_table_writer_0 = module_0.SearchTableWriter()
    assert f'{type(search_table_writer_0).__module__}.{type(search_table_writer_0).__qualname__}' == 'snippet_236.SearchTableWriter'
    bytes_0 = b'\x03\xdd\xa6'
    str_0 = '{(5fo4=d3n5[aF*6Ok'
    search_table_writer_0.build_search_otu_table(str_0, bytes_0, bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    dict_0 = {}
    search_table_writer_0 = module_0.SearchTableWriter()
    assert f'{type(search_table_writer_0).__module__}.{type(search_table_writer_0).__qualname__}' == 'snippet_236.SearchTableWriter'
    search_table_writer_0.build_search_otu_table(dict_0, dict_0, search_table_writer_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    search_table_writer_0 = module_0.SearchTableWriter()
    assert f'{type(search_table_writer_0).__module__}.{type(search_table_writer_0).__qualname__}' == 'snippet_236.SearchTableWriter'
    search_table_writer_0.build_search_otu_table(none_type_0, none_type_0, none_type_0)

def test_case_3():
    dict_0 = {}
    search_table_writer_0 = module_0.SearchTableWriter()
    assert f'{type(search_table_writer_0).__module__}.{type(search_table_writer_0).__qualname__}' == 'snippet_236.SearchTableWriter'
    bytes_0 = b'\x03\xdd\xa6'
    search_table_writer_0.build_search_otu_table(dict_0, dict_0, bytes_0)