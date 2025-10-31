import pytest
import snippet_37 as module_0

def test_case_0():
    float_0 = -833.21
    velocity_indicator_0 = module_0.VelocityIndicator()
    assert f'{type(velocity_indicator_0).__module__}.{type(velocity_indicator_0).__qualname__}' == 'snippet_37.VelocityIndicator'
    str_0 = velocity_indicator_0.render(float_0, float_0)
    assert str_0 == '🐌 Slow'

def test_case_1():
    int_0 = 166
    velocity_indicator_0 = module_0.VelocityIndicator()
    assert f'{type(velocity_indicator_0).__module__}.{type(velocity_indicator_0).__qualname__}' == 'snippet_37.VelocityIndicator'
    str_0 = velocity_indicator_0.render(int_0)
    assert str_0 == '🚀'

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = '<\r[hr"2zhqAVx(=>\tG'
    dict_0 = {str_0: str_0}
    velocity_indicator_0 = module_0.VelocityIndicator()
    assert f'{type(velocity_indicator_0).__module__}.{type(velocity_indicator_0).__qualname__}' == 'snippet_37.VelocityIndicator'
    velocity_indicator_0.render(dict_0)

def test_case_3():
    bool_0 = True
    velocity_indicator_0 = module_0.VelocityIndicator()
    assert f'{type(velocity_indicator_0).__module__}.{type(velocity_indicator_0).__qualname__}' == 'snippet_37.VelocityIndicator'
    str_0 = velocity_indicator_0.get_velocity_description(bool_0)
    assert str_0 == 'Slow'