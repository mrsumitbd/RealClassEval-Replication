import pytest
import snippet_297 as module_0
import codecs as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    m_a_s_visualizer_0 = module_0.MASVisualizer()
    assert f'{type(m_a_s_visualizer_0).__module__}.{type(m_a_s_visualizer_0).__qualname__}' == 'snippet_297.MASVisualizer'
    assert f'{type(m_a_s_visualizer_0.output_dir).__module__}.{type(m_a_s_visualizer_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    module_0.MASVisualizer(m_a_s_visualizer_0)

def test_case_1():
    m_a_s_visualizer_0 = module_0.MASVisualizer()
    assert f'{type(m_a_s_visualizer_0).__module__}.{type(m_a_s_visualizer_0).__qualname__}' == 'snippet_297.MASVisualizer'
    assert f'{type(m_a_s_visualizer_0.output_dir).__module__}.{type(m_a_s_visualizer_0.output_dir).__qualname__}' == 'pathlib.PosixPath'

@pytest.mark.xfail(strict=True)
def test_case_2():
    m_a_s_visualizer_0 = module_0.MASVisualizer()
    assert f'{type(m_a_s_visualizer_0).__module__}.{type(m_a_s_visualizer_0).__qualname__}' == 'snippet_297.MASVisualizer'
    assert f'{type(m_a_s_visualizer_0.output_dir).__module__}.{type(m_a_s_visualizer_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    m_a_s_visualizer_0.generate_html(m_a_s_visualizer_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    m_a_s_visualizer_0 = module_0.MASVisualizer()
    assert f'{type(m_a_s_visualizer_0).__module__}.{type(m_a_s_visualizer_0).__qualname__}' == 'snippet_297.MASVisualizer'
    assert f'{type(m_a_s_visualizer_0.output_dir).__module__}.{type(m_a_s_visualizer_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    none_type_0 = None
    var_0 = m_a_s_visualizer_0.generate_html(none_type_0)
    assert var_0 == '<html><body><h1>No visualization data available</h1></body></html>'
    m_a_s_visualizer_0.generate_html(var_0)

def test_case_4():
    buffered_incremental_decoder_0 = module_1.BufferedIncrementalDecoder()
    assert f'{type(buffered_incremental_decoder_0).__module__}.{type(buffered_incremental_decoder_0).__qualname__}' == 'codecs.BufferedIncrementalDecoder'
    assert buffered_incremental_decoder_0.errors == 'strict'
    assert buffered_incremental_decoder_0.buffer == b''
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
    m_a_s_visualizer_0 = module_0.MASVisualizer()
    assert f'{type(m_a_s_visualizer_0).__module__}.{type(m_a_s_visualizer_0).__qualname__}' == 'snippet_297.MASVisualizer'
    assert f'{type(m_a_s_visualizer_0.output_dir).__module__}.{type(m_a_s_visualizer_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    var_0 = buffered_incremental_decoder_0.getstate()
    var_1 = m_a_s_visualizer_0.generate_html(var_0)
    assert var_1 == '<html><body><h1>No visualization data available</h1></body></html>'