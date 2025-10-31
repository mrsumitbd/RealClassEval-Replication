import bs4 as module_0
import snippet_152 as module_1

def test_case_0():
    beautiful_stone_soup_0 = module_0.BeautifulStoneSoup()
    assert f'{type(module_0.builder_registry).__module__}.{type(module_0.builder_registry).__qualname__}' == 'bs4.builder.TreeBuilderRegistry'
    assert f'{type(module_0.builder_registry.builders_for_feature).__module__}.{type(module_0.builder_registry.builders_for_feature).__qualname__}' == 'collections.defaultdict'
    assert len(module_0.builder_registry.builders_for_feature) == 9
    assert f'{type(module_0.builder_registry.builders).__module__}.{type(module_0.builder_registry.builders).__qualname__}' == 'builtins.list'
    assert len(module_0.builder_registry.builders) == 3
    assert module_0.DEFAULT_OUTPUT_ENCODING == 'utf-8'
    assert module_0.PYTHON_SPECIFIC_ENCODINGS == {'raw_unicode_escape', 'undefined', 'string-escape', 'idna', 'palmos', 'oem', 'string_escape', 'raw-unicode-escape', 'unicode-escape', 'punycode', 'mbcs', 'unicode_escape'}
    module_1._FakeParent(beautiful_stone_soup_0)

def test_case_1():
    none_type_0 = None
    fake_parent_0 = module_1._FakeParent(none_type_0)
    fake_parent_0.__len__()