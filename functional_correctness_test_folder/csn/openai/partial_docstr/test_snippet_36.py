import pytest
import snippet_36 as module_0
import dataclasses as module_1
import spacy.tokens.span as module_2

def test_case_0():
    bool_0 = True
    int_0 = -620
    bool_1 = True
    int_1 = 2508
    set_0 = {bool_1, int_1}
    int_2 = -391
    sentence_0 = module_0.Sentence(bool_0, int_0, bool_0, set_0, int_2)
    assert f'{type(sentence_0).__module__}.{type(sentence_0).__qualname__}' == 'snippet_36.Sentence'
    assert sentence_0.start is True
    assert sentence_0.end == -620
    assert sentence_0.sent_id is True
    assert sentence_0.phrases == {True, 2508}
    assert sentence_0.distance == -391
    bool_2 = sentence_0.empty()
    assert bool_2 is False

@pytest.mark.xfail(strict=True)
def test_case_1():
    float_0 = -2171.93128
    str_0 = 'M3}{,msJDU\x0b\x0c.M'
    int_0 = -2126
    set_0 = {int_0, int_0, int_0}
    bool_0 = False
    sentence_0 = module_0.Sentence(int_0, int_0, int_0, set_0, bool_0)
    assert f'{type(sentence_0).__module__}.{type(sentence_0).__qualname__}' == 'snippet_36.Sentence'
    assert sentence_0.start == -2126
    assert sentence_0.end == -2126
    assert sentence_0.sent_id == -2126
    assert sentence_0.phrases == {-2126}
    assert sentence_0.distance is False
    bool_1 = sentence_0.empty()
    assert bool_1 is False
    int_1 = -574
    var_0 = module_1.dataclass(repr=float_0, match_args=float_0)
    assert f'{type(module_1.MISSING).__module__}.{type(module_1.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_1.KW_ONLY).__module__}.{type(module_1.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    sentence_1 = module_0.Sentence(int_1, float_0, var_0, float_0, str_0)
    assert f'{type(sentence_1).__module__}.{type(sentence_1).__qualname__}' == 'snippet_36.Sentence'
    assert sentence_1.start == -574
    assert sentence_1.end == pytest.approx(-2171.93128, abs=0.01, rel=0.01)
    assert sentence_1.phrases == pytest.approx(-2171.93128, abs=0.01, rel=0.01)
    assert sentence_1.distance == 'M3}{,msJDU\x0b\x0c.M'
    sentence_1.text(var_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    module_2.Span()