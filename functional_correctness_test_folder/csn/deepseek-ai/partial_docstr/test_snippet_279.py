import snippet_279 as module_0

def test_case_0():
    set_0 = set()
    search_dumper_ext_0 = module_0.SearchDumperExt(*set_0)
    assert f'{type(search_dumper_ext_0).__module__}.{type(search_dumper_ext_0).__qualname__}' == 'snippet_279.SearchDumperExt'
    search_dumper_ext_0.dump(search_dumper_ext_0, set_0)

def test_case_1():
    int_0 = -2270
    search_dumper_ext_0 = module_0.SearchDumperExt()
    assert f'{type(search_dumper_ext_0).__module__}.{type(search_dumper_ext_0).__qualname__}' == 'snippet_279.SearchDumperExt'
    search_dumper_ext_0.load(int_0, int_0)