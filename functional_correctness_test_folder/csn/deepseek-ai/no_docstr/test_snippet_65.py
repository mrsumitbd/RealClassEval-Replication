import pytest
import snippet_65 as module_0
import builtins as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'A5Ce9kjT\x0bl">hAQk'
    module_0.Tokenizer(str_0)

def test_case_1():
    object_0 = module_1.object()
    str_0 = '5[2D"DMthKpE'
    dict_0 = {object_0: str_0, str_0: str_0, object_0: object_0}
    tokenizer_0 = module_0.Tokenizer(join_broken_num=dict_0)
    assert f'{type(tokenizer_0).__module__}.{type(tokenizer_0).__qualname__}' == 'snippet_65.Tokenizer'
    assert module_0.DEFAULT_SENT_TOKENIZE_ENGINE == 'crfcut'
    assert module_0.DEFAULT_SUBWORD_TOKENIZE_ENGINE == 'tcc'
    assert f'{type(module_0.DEFAULT_SYLLABLE_DICT_TRIE).__module__}.{type(module_0.DEFAULT_SYLLABLE_DICT_TRIE).__qualname__}' == 'pythainlp.util.trie.Trie'
    assert len(module_0.DEFAULT_SYLLABLE_DICT_TRIE) == 10322
    assert module_0.DEFAULT_SYLLABLE_TOKENIZE_ENGINE == 'han_solo'
    assert f'{type(module_0.DEFAULT_WORD_DICT_TRIE).__module__}.{type(module_0.DEFAULT_WORD_DICT_TRIE).__qualname__}' == 'pythainlp.util.trie.Trie'
    assert len(module_0.DEFAULT_WORD_DICT_TRIE) == 62079
    assert module_0.DEFAULT_WORD_TOKENIZE_ENGINE == 'newmm'

def test_case_2():
    str_0 = 'ofu1Kt~R!'
    with pytest.raises(NotImplementedError):
        module_0.Tokenizer(engine=str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    int_0 = 1724
    tokenizer_0 = module_0.Tokenizer()
    assert f'{type(tokenizer_0).__module__}.{type(tokenizer_0).__qualname__}' == 'snippet_65.Tokenizer'
    assert module_0.DEFAULT_SENT_TOKENIZE_ENGINE == 'crfcut'
    assert module_0.DEFAULT_SUBWORD_TOKENIZE_ENGINE == 'tcc'
    assert f'{type(module_0.DEFAULT_SYLLABLE_DICT_TRIE).__module__}.{type(module_0.DEFAULT_SYLLABLE_DICT_TRIE).__qualname__}' == 'pythainlp.util.trie.Trie'
    assert len(module_0.DEFAULT_SYLLABLE_DICT_TRIE) == 10322
    assert module_0.DEFAULT_SYLLABLE_TOKENIZE_ENGINE == 'han_solo'
    assert f'{type(module_0.DEFAULT_WORD_DICT_TRIE).__module__}.{type(module_0.DEFAULT_WORD_DICT_TRIE).__qualname__}' == 'pythainlp.util.trie.Trie'
    assert len(module_0.DEFAULT_WORD_DICT_TRIE) == 62079
    assert module_0.DEFAULT_WORD_TOKENIZE_ENGINE == 'newmm'
    tokenizer_0.word_tokenize(int_0)

def test_case_4():
    str_0 = 'bIO0{.'
    int_0 = 1797
    tokenizer_0 = module_0.Tokenizer(keep_whitespace=int_0)
    assert f'{type(tokenizer_0).__module__}.{type(tokenizer_0).__qualname__}' == 'snippet_65.Tokenizer'
    assert module_0.DEFAULT_SENT_TOKENIZE_ENGINE == 'crfcut'
    assert module_0.DEFAULT_SUBWORD_TOKENIZE_ENGINE == 'tcc'
    assert f'{type(module_0.DEFAULT_SYLLABLE_DICT_TRIE).__module__}.{type(module_0.DEFAULT_SYLLABLE_DICT_TRIE).__qualname__}' == 'pythainlp.util.trie.Trie'
    assert len(module_0.DEFAULT_SYLLABLE_DICT_TRIE) == 10322
    assert module_0.DEFAULT_SYLLABLE_TOKENIZE_ENGINE == 'han_solo'
    assert f'{type(module_0.DEFAULT_WORD_DICT_TRIE).__module__}.{type(module_0.DEFAULT_WORD_DICT_TRIE).__qualname__}' == 'pythainlp.util.trie.Trie'
    assert len(module_0.DEFAULT_WORD_DICT_TRIE) == 62079
    assert module_0.DEFAULT_WORD_TOKENIZE_ENGINE == 'newmm'
    tokenizer_0.set_tokenize_engine(str_0)