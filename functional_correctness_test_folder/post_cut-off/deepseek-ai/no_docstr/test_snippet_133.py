import pytest
import snippet_133 as module_0

def test_case_0():
    float_0 = 1136.19
    text_border_0 = module_0.Text_border(width=float_0)
    assert f'{type(text_border_0).__module__}.{type(text_border_0).__qualname__}' == 'snippet_133.Text_border'
    assert text_border_0.alpha == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert f'{type(text_border_0.color).__module__}.{type(text_border_0.color).__qualname__}' == 'builtins.tuple'
    assert len(text_border_0.color) == 3
    assert text_border_0.width == pytest.approx(2.27238, abs=0.01, rel=0.01)

def test_case_1():
    text_border_0 = module_0.Text_border()
    assert f'{type(text_border_0).__module__}.{type(text_border_0).__qualname__}' == 'snippet_133.Text_border'
    assert text_border_0.alpha == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert f'{type(text_border_0.color).__module__}.{type(text_border_0.color).__qualname__}' == 'builtins.tuple'
    assert len(text_border_0.color) == 3
    assert text_border_0.width == pytest.approx(0.08000000000000002, abs=0.01, rel=0.01)
    text_border_0.export_json()