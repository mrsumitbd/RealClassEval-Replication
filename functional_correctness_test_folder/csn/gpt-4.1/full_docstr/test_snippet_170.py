import pytest
import snippet_170 as module_0

def test_case_0():
    int_0 = 1613
    metrics_d_a_o_0 = module_0.MetricsDAO()
    assert f'{type(metrics_d_a_o_0).__module__}.{type(metrics_d_a_o_0).__qualname__}' == 'snippet_170.MetricsDAO'
    with pytest.raises(NotImplementedError):
        metrics_d_a_o_0.get(int_0, int_0)

def test_case_1():
    complex_0 = -668 - 976j
    metrics_d_a_o_0 = module_0.MetricsDAO()
    assert f'{type(metrics_d_a_o_0).__module__}.{type(metrics_d_a_o_0).__qualname__}' == 'snippet_170.MetricsDAO'
    with pytest.raises(NotImplementedError):
        metrics_d_a_o_0.delete(complex_0)