import pytest
import snippet_77 as module_0
import codecs as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '4wO7mrJ]^6'
    xinyu_search_a_p_i_0 = module_0.XinyuSearchAPI(str_0, str_0)
    xinyu_search_a_p_i_0.query_detail()

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '4wO7mrJ]^6'
    xinyu_search_a_p_i_0 = module_0.XinyuSearchAPI(str_0, str_0)
    bool_0 = False
    xinyu_search_a_p_i_0.search(bool_0)

def test_case_2():
    str_0 = 'e3B?<]SV j"\\'
    module_0.XinyuSearchAPI(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    str_0 = 'oDbUk'
    xinyu_search_a_p_i_0 = module_0.XinyuSearchAPI(none_type_0, str_0)
    str_1 = '\\\n`Wp%Cw\r]e#to\rhZ,k'
    buffered_incremental_decoder_0 = module_1.BufferedIncrementalDecoder(none_type_0)
    assert module_1.BOM_UTF8 == b'\xef\xbb\xbf'
    assert module_1.BOM_LE == b'\xff\xfe'
    assert module_1.BOM_UTF16_LE == b'\xff\xfe'
    assert module_1.BOM_BE == b'\xfe\xff'
    assert module_1.BOM_UTF16_BE == b'\xfe\xff'
    assert module_1.BOM_UTF32_LE == b'\xff\xfe\x00\x00'
    assert module_1.BOM_UTF32_BE == b'\x00\x00\xfe\xff'
    assert module_1.BOM == b'\xff\xfe'
    assert module_1.BOM_UTF16 == b'\xff\xfe'
    assert module_1.BOM_UTF32 == b'\xff\xfe\x00\x00'
    assert module_1.BOM32_LE == b'\xff\xfe'
    assert module_1.BOM32_BE == b'\xfe\xff'
    assert module_1.BOM64_LE == b'\xff\xfe\x00\x00'
    assert module_1.BOM64_BE == b'\x00\x00\xfe\xff'
    xinyu_search_a_p_i_0.search(str_1, buffered_incremental_decoder_0)