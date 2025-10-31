import pytest
import snippet_222 as module_0

def test_case_0():
    none_type_0 = None
    transport_0 = module_0.Transport(none_type_0, none_type_0, reconnect_timeout=none_type_0)
    assert f'{type(transport_0).__module__}.{type(transport_0).__qualname__}' == 'snippet_222.Transport'
    assert transport_0.can_log is False
    assert transport_0.connect_task is None
    assert transport_0.gateway is None
    assert transport_0.protocol is None
    assert transport_0.reconnect_timeout is None
    assert transport_0.timeout == pytest.approx(1.0, abs=0.01, rel=0.01)
    transport_0.disconnect()

def test_case_1():
    none_type_0 = None
    transport_0 = module_0.Transport(none_type_0, none_type_0, reconnect_timeout=none_type_0)
    assert f'{type(transport_0).__module__}.{type(transport_0).__qualname__}' == 'snippet_222.Transport'
    assert transport_0.can_log is False
    assert transport_0.connect_task is None
    assert transport_0.gateway is None
    assert transport_0.protocol is None
    assert transport_0.reconnect_timeout is None
    assert transport_0.timeout == pytest.approx(1.0, abs=0.01, rel=0.01)
    transport_0.send(transport_0)

def test_case_2():
    none_type_0 = None
    transport_0 = module_0.Transport(none_type_0, none_type_0, reconnect_timeout=none_type_0)
    assert f'{type(transport_0).__module__}.{type(transport_0).__qualname__}' == 'snippet_222.Transport'
    assert transport_0.can_log is False
    assert transport_0.connect_task is None
    assert transport_0.gateway is None
    assert transport_0.protocol is None
    assert transport_0.reconnect_timeout is None
    assert transport_0.timeout == pytest.approx(1.0, abs=0.01, rel=0.01)
    transport_0.send(none_type_0)
    transport_0.disconnect()