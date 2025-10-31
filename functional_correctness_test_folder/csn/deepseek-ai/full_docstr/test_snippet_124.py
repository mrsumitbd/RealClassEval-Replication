import pytest
import snippet_124 as module_0

def test_case_0():
    bool_0 = False
    delay_timer_0 = module_0.DelayTimer(bool_0)
    assert f'{type(delay_timer_0).__module__}.{type(delay_timer_0).__qualname__}' == 'snippet_124.DelayTimer'
    assert delay_timer_0.delay is False
    assert delay_timer_0.last_time == pytest.approx(1758853423.088362, abs=0.01, rel=0.01)
    var_0 = delay_timer_0.is_time()
    assert var_0 is True
    assert delay_timer_0.last_time == pytest.approx(1758853423.088502, abs=0.01, rel=0.01)

def test_case_1():
    bool_0 = True
    delay_timer_0 = module_0.DelayTimer(bool_0)
    assert f'{type(delay_timer_0).__module__}.{type(delay_timer_0).__qualname__}' == 'snippet_124.DelayTimer'
    assert delay_timer_0.delay is True
    assert delay_timer_0.last_time == pytest.approx(1758853423.088701, abs=0.01, rel=0.01)
    var_0 = delay_timer_0.is_time()
    assert var_0 is False

def test_case_2():
    bytes_0 = b'\xb4h6\x12\x08\xe8\x9e\xd8'
    delay_timer_0 = module_0.DelayTimer(bytes_0)
    assert f'{type(delay_timer_0).__module__}.{type(delay_timer_0).__qualname__}' == 'snippet_124.DelayTimer'
    assert delay_timer_0.delay == b'\xb4h6\x12\x08\xe8\x9e\xd8'
    assert delay_timer_0.last_time == pytest.approx(1758853423.088941, abs=0.01, rel=0.01)