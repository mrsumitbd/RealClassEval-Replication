import pytest
import snippet_290 as module_0
import zmq.constants as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    z_m_q_name_server_0 = module_0.ZMQNameServer()
    assert f'{type(z_m_q_name_server_0).__module__}.{type(z_m_q_name_server_0).__qualname__}' == 'snippet_290.ZMQNameServer'
    assert z_m_q_name_server_0.running is True
    assert z_m_q_name_server_0.listener is None
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.REP == module_1.SocketType.REP
    assert module_0.REQ == module_1.SocketType.REQ
    complex_0 = -1690.01 - 530.4105j
    z_m_q_name_server_0.run(z_m_q_name_server_0, complex_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    z_m_q_name_server_0 = module_0.ZMQNameServer()
    assert f'{type(z_m_q_name_server_0).__module__}.{type(z_m_q_name_server_0).__qualname__}' == 'snippet_290.ZMQNameServer'
    assert z_m_q_name_server_0.running is True
    assert z_m_q_name_server_0.listener is None
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.REP == module_1.SocketType.REP
    assert module_0.REQ == module_1.SocketType.REQ
    var_0 = z_m_q_name_server_0.stop()
    assert z_m_q_name_server_0.running is False
    z_m_q_name_server_0.close_sockets_and_threads()
    none_type_0 = None
    z_m_q_name_server_0.run(none_type_0)

def test_case_2():
    z_m_q_name_server_0 = module_0.ZMQNameServer()
    assert f'{type(z_m_q_name_server_0).__module__}.{type(z_m_q_name_server_0).__qualname__}' == 'snippet_290.ZMQNameServer'
    assert z_m_q_name_server_0.running is True
    assert z_m_q_name_server_0.listener is None
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.REP == module_1.SocketType.REP
    assert module_0.REQ == module_1.SocketType.REQ
    z_m_q_name_server_0.close_sockets_and_threads()

def test_case_3():
    z_m_q_name_server_0 = module_0.ZMQNameServer()
    assert f'{type(z_m_q_name_server_0).__module__}.{type(z_m_q_name_server_0).__qualname__}' == 'snippet_290.ZMQNameServer'
    assert z_m_q_name_server_0.running is True
    assert z_m_q_name_server_0.listener is None
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.REP == module_1.SocketType.REP
    assert module_0.REQ == module_1.SocketType.REQ
    var_0 = z_m_q_name_server_0.stop()
    assert z_m_q_name_server_0.running is False
    z_m_q_name_server_0.close_sockets_and_threads()

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = '8k;tqBB-ml4PpO+'
    z_m_q_name_server_0 = module_0.ZMQNameServer()
    assert f'{type(z_m_q_name_server_0).__module__}.{type(z_m_q_name_server_0).__qualname__}' == 'snippet_290.ZMQNameServer'
    assert z_m_q_name_server_0.running is True
    assert z_m_q_name_server_0.listener is None
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.REP == module_1.SocketType.REP
    assert module_0.REQ == module_1.SocketType.REQ
    z_m_q_name_server_0.run(str_0)