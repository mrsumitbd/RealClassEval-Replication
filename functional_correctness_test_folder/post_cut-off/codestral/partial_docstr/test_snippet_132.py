import pytest
import snippet_132 as module_0

def test_case_0():
    bytes_0 = b'\xe4\x9d\x17\xccW'
    text_background_0 = module_0.Text_background(color=bytes_0, width=bytes_0)
    assert f'{type(text_background_0).__module__}.{type(text_background_0).__qualname__}' == 'snippet_132.Text_background'
    assert text_background_0.style == 0
    assert text_background_0.alpha == pytest.approx(1.0, abs=0.01, rel=0.01)
    assert text_background_0.color == b'\xe4\x9d\x17\xccW'
    assert text_background_0.round_radius == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert text_background_0.height == pytest.approx(0.14, abs=0.01, rel=0.01)
    assert text_background_0.width == b'\xe4\x9d\x17\xccW'
    assert text_background_0.horizontal_offset == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert text_background_0.vertical_offset == pytest.approx(0.0, abs=0.01, rel=0.01)

def test_case_1():
    str_0 = 'gMe:'
    bool_0 = True
    bool_1 = False
    text_background_0 = module_0.Text_background(color=str_0, alpha=bool_0, height=bool_0, width=bool_1, vertical_offset=bool_1)
    assert f'{type(text_background_0).__module__}.{type(text_background_0).__qualname__}' == 'snippet_132.Text_background'
    assert text_background_0.style == 0
    assert text_background_0.alpha is True
    assert text_background_0.color == 'gMe:'
    assert text_background_0.round_radius == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert text_background_0.height is True
    assert text_background_0.width is False
    assert text_background_0.horizontal_offset == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert text_background_0.vertical_offset == -1
    text_background_0.export_json()