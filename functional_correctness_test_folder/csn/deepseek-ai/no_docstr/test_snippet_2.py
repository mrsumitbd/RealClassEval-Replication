import pytest
import snippet_2 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    module_0.OcrQualityDictionary(wordlist=none_type_0)

def test_case_1():
    str_0 = 'RkE0|i+v>h)f0lYa!AV'
    ocr_quality_dictionary_0 = module_0.OcrQualityDictionary(wordlist=str_0)
    assert f'{type(ocr_quality_dictionary_0).__module__}.{type(ocr_quality_dictionary_0).__qualname__}' == 'snippet_2.OcrQualityDictionary'
    assert ocr_quality_dictionary_0.dictionary == {'A', 'v', 'V', 'k', 'i', 'f', 'E', 'a', '!', '|', '+', 'h', 'R', ')', '0', 'Y', 'l', '>'}
    float_0 = ocr_quality_dictionary_0.measure_words_matched(str_0)
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)

def test_case_2():
    str_0 = 'RkE0|i+v>hcf0lYa!AV'
    ocr_quality_dictionary_0 = module_0.OcrQualityDictionary(wordlist=str_0)
    assert f'{type(ocr_quality_dictionary_0).__module__}.{type(ocr_quality_dictionary_0).__qualname__}' == 'snippet_2.OcrQualityDictionary'
    assert ocr_quality_dictionary_0.dictionary == {'A', 'v', 'V', 'k', 'i', 'f', 'E', 'a', '!', 'c', '|', '+', 'h', 'R', '0', 'Y', 'l', '>'}
    float_0 = ocr_quality_dictionary_0.measure_words_matched(str_0)
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)