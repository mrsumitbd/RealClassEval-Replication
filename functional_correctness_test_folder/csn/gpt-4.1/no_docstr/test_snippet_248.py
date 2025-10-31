import pytest
import snippet_248 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    parser_0 = module_0.Parser()
    assert f'{type(parser_0).__module__}.{type(parser_0).__qualname__}' == 'snippet_248.Parser'
    parser_0.load_from_file(parser_0)

def test_case_1():
    parser_0 = module_0.Parser()
    assert f'{type(parser_0).__module__}.{type(parser_0).__qualname__}' == 'snippet_248.Parser'
    with pytest.raises(ValueError):
        parser_0.load_from_file(parser_0, parser_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = ':b'
    parser_0 = module_0.Parser()
    assert f'{type(parser_0).__module__}.{type(parser_0).__qualname__}' == 'snippet_248.Parser'
    parser_0.load_from_file(str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = ':b'
    parser_0 = module_0.Parser()
    assert f'{type(parser_0).__module__}.{type(parser_0).__qualname__}' == 'snippet_248.Parser'
    parser_0.load_all_from_directory(str_0)
    parser_0.load_from_file(str_0)

def test_case_4():
    str_0 = '6*N.\x0c+<>'
    parser_0 = module_0.Parser()
    assert f'{type(parser_0).__module__}.{type(parser_0).__qualname__}' == 'snippet_248.Parser'
    with pytest.raises(ValueError):
        parser_0.load_from_file(str_0)