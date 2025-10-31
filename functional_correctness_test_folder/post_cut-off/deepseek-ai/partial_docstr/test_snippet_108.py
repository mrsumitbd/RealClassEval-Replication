import pytest
import snippet_108 as module_0
import re as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '+7'
    module_0.RecursiveLevel(pattern=str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '+7'
    list_0 = [str_0]
    recursive_level_0 = module_0.RecursiveLevel(list_0)
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters == ['+7']
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim == 'prev'
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'
    str_1 = recursive_level_0.__repr__()
    assert str_1 == "RecursiveLevel(delimiters=['+7'], whitespace=False, include_delim=prev, pattern=None, pattern_mode=split)"
    module_0.RecursiveLevel(pattern=str_0)

def test_case_2():
    recursive_level_0 = module_0.RecursiveLevel()
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters is None
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim == 'prev'
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'
    recursive_level_0.to_dict()

def test_case_3():
    none_type_0 = None
    recursive_level_0 = module_0.RecursiveLevel(include_delim=none_type_0, pattern=none_type_0)
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters is None
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim is None
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = '+7'
    list_0 = [str_0]
    recursive_level_0 = module_0.RecursiveLevel(list_0)
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters == ['+7']
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim == 'prev'
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'
    module_0.RecursiveLevel(pattern=str_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = ''
    list_0 = module_1.escape(str_0)
    assert list_0 == ''
    assert module_1.ASCII == module_1.RegexFlag.ASCII
    assert module_1.A == module_1.RegexFlag.ASCII
    assert module_1.IGNORECASE == module_1.RegexFlag.IGNORECASE
    assert module_1.I == module_1.RegexFlag.IGNORECASE
    assert module_1.LOCALE == module_1.RegexFlag.LOCALE
    assert module_1.L == module_1.RegexFlag.LOCALE
    assert module_1.UNICODE == module_1.RegexFlag.UNICODE
    assert module_1.U == module_1.RegexFlag.UNICODE
    assert module_1.MULTILINE == module_1.RegexFlag.MULTILINE
    assert module_1.M == module_1.RegexFlag.MULTILINE
    assert module_1.DOTALL == module_1.RegexFlag.DOTALL
    assert module_1.S == module_1.RegexFlag.DOTALL
    assert module_1.VERBOSE == module_1.RegexFlag.VERBOSE
    assert module_1.X == module_1.RegexFlag.VERBOSE
    assert module_1.TEMPLATE == module_1.RegexFlag.TEMPLATE
    assert module_1.T == module_1.RegexFlag.TEMPLATE
    assert module_1.DEBUG == module_1.RegexFlag.DEBUG
    module_0.RecursiveLevel(list_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = '{c('
    recursive_level_0 = module_0.RecursiveLevel(str_0)
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters == '{c('
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim == 'prev'
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'
    str_1 = "QmVW?q@'dWm<#"
    list_0 = [str_1]
    bool_0 = False
    recursive_level_1 = module_0.RecursiveLevel(list_0, bool_0, list_0)
    assert f'{type(recursive_level_1).__module__}.{type(recursive_level_1).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_1.delimiters == ["QmVW?q@'dWm<#"]
    assert recursive_level_1.whitespace is False
    assert recursive_level_1.include_delim == ["QmVW?q@'dWm<#"]
    assert recursive_level_1.pattern is None
    assert recursive_level_1.pattern_mode == 'split'
    module_0.RecursiveLevel(pattern=str_0, pattern_mode=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    str_0 = '{c\t'
    recursive_level_0 = module_0.RecursiveLevel(str_0)
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters == '{c\t'
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim == 'prev'
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'
    str_1 = "QmVW?q@'dWm<#"
    list_0 = [str_0, str_1]
    bool_0 = True
    module_0.RecursiveLevel(list_0, bool_0, list_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    bool_0 = True
    none_type_0 = None
    module_0.RecursiveLevel(whitespace=bool_0, pattern_mode=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    bool_0 = False
    tuple_0 = (bool_0,)
    module_0.RecursiveLevel(pattern=tuple_0)

@pytest.mark.xfail(strict=True)
def test_case_10():
    str_0 = ''
    list_0 = [str_0]
    module_0.RecursiveLevel(list_0)

@pytest.mark.xfail(strict=True)
def test_case_11():
    str_0 = '{c\t'
    recursive_level_0 = module_0.RecursiveLevel(str_0)
    assert f'{type(recursive_level_0).__module__}.{type(recursive_level_0).__qualname__}' == 'snippet_108.RecursiveLevel'
    assert recursive_level_0.delimiters == '{c\t'
    assert recursive_level_0.whitespace is False
    assert recursive_level_0.include_delim == 'prev'
    assert recursive_level_0.pattern is None
    assert recursive_level_0.pattern_mode == 'split'
    assert module_0.RecursiveLevel.delimiters is None
    assert module_0.RecursiveLevel.whitespace is False
    assert module_0.RecursiveLevel.include_delim == 'prev'
    assert module_0.RecursiveLevel.pattern is None
    assert module_0.RecursiveLevel.pattern_mode == 'split'
    assert f'{type(module_0.RecursiveLevel.from_dict).__module__}.{type(module_0.RecursiveLevel.from_dict).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.RecursiveLevel.from_recipe).__module__}.{type(module_0.RecursiveLevel.from_recipe).__qualname__}' == 'builtins.method'
    recursive_level_0.to_dict()
    var_0 = recursive_level_0.__eq__(str_0)
    str_1 = "QmVW?q@'dWm<#"
    list_0 = [str_1, var_0]
    bool_0 = False
    module_0.RecursiveLevel(list_0, bool_0, list_0)

@pytest.mark.xfail(strict=True)
def test_case_12():
    str_0 = ''
    module_0.RecursiveLevel(pattern=str_0)