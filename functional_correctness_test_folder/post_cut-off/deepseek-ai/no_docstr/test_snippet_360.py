import pytest
import snippet_360 as module_0
import dataclasses as module_1

def test_case_0():
    str_0 = 'q8bDl],J*\x0cqKWJ{jfKgV'
    str_1 = '\x0b?{'
    str_2 = "9'd;\nZd<?*F_h\x0ceY@5"
    none_type_0 = None
    search_result_0 = module_0.SearchResult(str_2, none_type_0, none_type_0, none_type_0, none_type_0, none_type_0)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == "9'd;\nZd<?*F_h\x0ceY@5"
    assert search_result_0.start is None
    assert search_result_0.end is None
    assert search_result_0.class_name is None
    assert search_result_0.func_name is None
    assert search_result_0.code is None
    str_3 = search_result_0.to_relative_path(str_0, str_1)
    assert str_3 == 'q8bDl],J*\x0cqKWJ{jfKgV'

def test_case_1():
    str_0 = '#;.[3Wtt#UZ6":!\x0c\tGY'
    str_1 = '_V$eZ7^\x0b:N'
    str_2 = 'sI'
    none_type_0 = None
    search_result_0 = module_0.SearchResult(str_2, none_type_0, none_type_0, none_type_0, str_1, str_2)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == 'sI'
    assert search_result_0.start is None
    assert search_result_0.end is None
    assert search_result_0.class_name is None
    assert search_result_0.func_name == '_V$eZ7^\x0b:N'
    assert search_result_0.code == 'sI'
    search_result_1 = module_0.SearchResult(str_1, str_1, str_1, str_1, str_1, search_result_0)
    assert f'{type(search_result_1).__module__}.{type(search_result_1).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_1.file_path == '_V$eZ7^\x0b:N'
    assert search_result_1.start == '_V$eZ7^\x0b:N'
    assert search_result_1.end == '_V$eZ7^\x0b:N'
    assert search_result_1.class_name == '_V$eZ7^\x0b:N'
    assert search_result_1.func_name == '_V$eZ7^\x0b:N'
    assert f'{type(search_result_1.code).__module__}.{type(search_result_1.code).__qualname__}' == 'snippet_360.SearchResult'
    var_0 = search_result_1.to_tagged_upto_func(str_0)
    assert var_0 == '<file>_V$eZ7^\x0b:N</file>\n<class>_V$eZ7^\x0b:N</class><func>_V$eZ7^\x0b:N</func>'

def test_case_2():
    str_0 = 'xP&?\rET\n'
    str_1 = ':4\x0bzd5N-u2}v?'
    none_type_0 = None
    str_2 = '(gG'
    search_result_0 = module_0.SearchResult(str_1, none_type_0, none_type_0, none_type_0, str_1, str_2)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == ':4\x0bzd5N-u2}v?'
    assert search_result_0.start is None
    assert search_result_0.end is None
    assert search_result_0.class_name is None
    assert search_result_0.func_name == ':4\x0bzd5N-u2}v?'
    assert search_result_0.code == '(gG'
    var_0 = search_result_0.to_tagged_upto_func(str_0)
    assert var_0 == '<file>:4\x0bzd5N-u2}v?</file>\n<func>:4\x0bzd5N-u2}v?</func>'

def test_case_3():
    str_0 = 'Kn\x0c\r'
    none_type_0 = None
    bool_0 = False
    search_result_0 = module_0.SearchResult(str_0, str_0, none_type_0, str_0, none_type_0, bool_0)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == 'Kn\x0c\r'
    assert search_result_0.start == 'Kn\x0c\r'
    assert search_result_0.end is None
    assert search_result_0.class_name == 'Kn\x0c\r'
    assert search_result_0.func_name is None
    assert search_result_0.code is False
    tuple_0 = ()
    str_1 = search_result_0.collapse_to_file_level(tuple_0, str_0)
    assert str_1 == ''
    var_0 = search_result_0.to_tagged_str(str_0)
    assert var_0 == '<file>Kn\x0c\r</file>\n<class>Kn\x0c\r</class>\n<code>\nFalse\n</code>'

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = 'Kn\x0c\r'
    none_type_0 = None
    bool_0 = False
    search_result_0 = module_0.SearchResult(str_0, str_0, none_type_0, str_0, none_type_0, bool_0)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == 'Kn\x0c\r'
    assert search_result_0.start == 'Kn\x0c\r'
    assert search_result_0.end is None
    assert search_result_0.class_name == 'Kn\x0c\r'
    assert search_result_0.func_name is None
    assert search_result_0.code is False
    str_1 = 'R4\\<G\n'
    var_0 = search_result_0.to_tagged_str(str_1)
    assert var_0 == '<file>Kn\x0c\r</file>\n<class>Kn\x0c\r</class>\n<code>\nFalse\n</code>'
    search_result_0.collapse_to_method_level(var_0, var_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = 'KRn\x0c\r'
    none_type_0 = None
    bool_0 = False
    search_result_0 = module_0.SearchResult(str_0, str_0, none_type_0, str_0, none_type_0, bool_0)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == 'KRn\x0c\r'
    assert search_result_0.start == 'KRn\x0c\r'
    assert search_result_0.end is None
    assert search_result_0.class_name == 'KRn\x0c\r'
    assert search_result_0.func_name is None
    assert search_result_0.code is False
    var_0 = search_result_0.to_tagged_str(str_0)
    assert var_0 == '<file>KRn\x0c\r</file>\n<class>KRn\x0c\r</class>\n<code>\nFalse\n</code>'
    search_result_0.collapse_to_file_level(var_0, var_0)

def test_case_6():
    str_0 = '\x0c\r'
    none_type_0 = None
    search_result_0 = module_0.SearchResult(str_0, none_type_0, none_type_0, none_type_0, none_type_0, none_type_0)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == '\x0c\r'
    assert search_result_0.start is None
    assert search_result_0.end is None
    assert search_result_0.class_name is None
    assert search_result_0.func_name is None
    assert search_result_0.code is None
    str_1 = 'R4\\<G\n'
    tuple_0 = ()
    str_2 = search_result_0.collapse_to_method_level(tuple_0, str_1)
    assert str_2 == ''

@pytest.mark.xfail(strict=True)
def test_case_7():
    str_0 = '\x0c\r'
    none_type_0 = None
    none_type_1 = None
    search_result_0 = module_0.SearchResult(str_0, none_type_0, none_type_0, none_type_0, none_type_1, none_type_0)
    assert f'{type(search_result_0).__module__}.{type(search_result_0).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_0.file_path == '\x0c\r'
    assert search_result_0.start is None
    assert search_result_0.end is None
    assert search_result_0.class_name is None
    assert search_result_0.func_name is None
    assert search_result_0.code is None
    str_1 = '/ynR4\\<\n'
    var_0 = module_1.dataclass(init=str_0, frozen=search_result_0, kw_only=search_result_0)
    assert f'{type(module_1.MISSING).__module__}.{type(module_1.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_1.KW_ONLY).__module__}.{type(module_1.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    search_result_1 = module_0.SearchResult(str_1, var_0, none_type_0, str_0, none_type_0, str_0)
    assert f'{type(search_result_1).__module__}.{type(search_result_1).__qualname__}' == 'snippet_360.SearchResult'
    assert search_result_1.file_path == '/ynR4\\<\n'
    assert search_result_1.end is None
    assert search_result_1.class_name == '\x0c\r'
    assert search_result_1.func_name is None
    assert search_result_1.code == '\x0c\r'
    tuple_0 = ()
    str_2 = search_result_0.collapse_to_file_level(tuple_0, str_0)
    assert str_2 == ''
    var_1 = search_result_0.to_tagged_str(str_0)
    assert var_1 == '<file>\x0c\r</file>\n\n<code>\nNone\n</code>'
    str_3 = search_result_0.collapse_to_method_level(tuple_0, str_2)
    assert str_3 == ''
    search_result_1.to_tagged_str(search_result_1)