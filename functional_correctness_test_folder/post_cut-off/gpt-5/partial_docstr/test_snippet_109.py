import pytest
import snippet_109 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'o'
    bool_0 = True
    set_0 = {bool_0, bool_0, str_0}
    module_0.Sentence(str_0, str_0, bool_0, set_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = 1822
    module_0.Sentence(int_0, int_0, int_0, int_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = '%2USDK[0Rxun'
    bool_0 = False
    bool_1 = True
    module_0.Sentence(str_0, bool_0, bool_1, str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    bytes_0 = b"\xa0B\xa2\xb2n\x99x\xfdZ\xcaO\n\xa5'\x01\xa4\x82\xd6\xc1\x99"
    str_0 = ''
    bool_0 = False
    module_0.Sentence(str_0, bool_0, bytes_0, bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = ';mLB}d'
    bool_0 = False
    int_0 = -26
    none_type_0 = None
    module_0.Sentence(str_0, bool_0, int_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = 'W}\nVtjQ4Na:uV'
    str_1 = '%2USDK[0Rxun'
    bool_0 = True
    sentence_0 = module_0.Sentence(str_1, bool_0, bool_0, bool_0)
    assert f'{type(sentence_0).__module__}.{type(sentence_0).__qualname__}' == 'snippet_109.Sentence'
    assert sentence_0.text == '%2USDK[0Rxun'
    assert sentence_0.start_index is True
    assert sentence_0.end_index is True
    assert sentence_0.token_count is True
    assert f'{type(module_0.Sentence.from_dict).__module__}.{type(module_0.Sentence.from_dict).__qualname__}' == 'builtins.method'
    str_2 = sentence_0.__repr__()
    assert str_2 == 'Sentence(text=%2USDK[0Rxun, start_index=True, end_index=True, token_count=True)'
    bool_1 = True
    none_type_0 = None
    module_0.Sentence(str_0, bool_1, none_type_0, bool_1)

@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = 'W}\nVtjQ4Na:uV'
    str_1 = '%2USDK[0Rxun'
    bool_0 = True
    sentence_0 = module_0.Sentence(str_1, bool_0, bool_0, bool_0)
    assert f'{type(sentence_0).__module__}.{type(sentence_0).__qualname__}' == 'snippet_109.Sentence'
    assert sentence_0.text == '%2USDK[0Rxun'
    assert sentence_0.start_index is True
    assert sentence_0.end_index is True
    assert sentence_0.token_count is True
    assert f'{type(module_0.Sentence.from_dict).__module__}.{type(module_0.Sentence.from_dict).__qualname__}' == 'builtins.method'
    sentence_0.to_dict()
    bool_1 = False
    none_type_0 = None
    module_0.Sentence(str_0, bool_1, none_type_0, bool_1)

@pytest.mark.xfail(strict=True)
def test_case_7():
    str_0 = "'5b<\r\tP`6F_*-=TV<n:"
    int_0 = -61
    int_1 = -62
    bool_0 = True
    module_0.Sentence(str_0, int_0, int_1, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    str_0 = 'W}\nVtjQ4Na:uV'
    str_1 = '%2USDK[0Rxun'
    bool_0 = False
    sentence_0 = module_0.Sentence(str_1, bool_0, bool_0, bool_0)
    assert f'{type(sentence_0).__module__}.{type(sentence_0).__qualname__}' == 'snippet_109.Sentence'
    assert sentence_0.text == '%2USDK[0Rxun'
    assert sentence_0.start_index is False
    assert sentence_0.end_index is False
    assert sentence_0.token_count is False
    assert f'{type(module_0.Sentence.from_dict).__module__}.{type(module_0.Sentence.from_dict).__qualname__}' == 'builtins.method'
    sentence_0.to_dict()
    str_2 = sentence_0.__repr__()
    assert str_2 == 'Sentence(text=%2USDK[0Rxun, start_index=False, end_index=False, token_count=False)'
    int_0 = 1256
    bool_1 = False
    module_0.Sentence(str_0, int_0, bool_1, int_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    bool_0 = False
    str_0 = '?# 1u1^k*!kQMLU&R'
    int_0 = 1573
    int_1 = -1157
    module_0.Sentence(str_0, bool_0, int_0, int_1)