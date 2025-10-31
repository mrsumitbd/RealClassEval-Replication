import pytest
import snippet_140 as module_0

def test_case_0():
    abstract_html_converter_0 = module_0.AbstractHtmlConverter()
    assert f'{type(abstract_html_converter_0).__module__}.{type(abstract_html_converter_0).__qualname__}' == 'snippet_140.AbstractHtmlConverter'
    with pytest.raises(NotImplementedError):
        abstract_html_converter_0.get_text(abstract_html_converter_0)