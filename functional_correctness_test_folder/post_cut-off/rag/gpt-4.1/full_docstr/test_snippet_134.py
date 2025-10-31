import pytest
import snippet_134 as module_0

def test_case_0():
    str_0 = ']%DKW+]'
    text_shadow_0 = module_0.Text_shadow(color=str_0, distance=str_0, smoothing=str_0)
    assert f'{type(text_shadow_0).__module__}.{type(text_shadow_0).__qualname__}' == 'snippet_134.Text_shadow'
    assert text_shadow_0.has_shadow is False
    assert text_shadow_0.alpha == pytest.approx(0.9, abs=0.01, rel=0.01)
    assert text_shadow_0.angle == pytest.approx(-45.0, abs=0.01, rel=0.01)
    assert text_shadow_0.color == ']%DKW+]'
    assert text_shadow_0.distance == ']%DKW+]'
    assert text_shadow_0.smoothing == ']%DKW+]'
    text_shadow_0.export_json()