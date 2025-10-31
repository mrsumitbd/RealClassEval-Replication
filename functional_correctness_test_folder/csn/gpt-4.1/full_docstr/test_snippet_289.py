import pytest
import snippet_289 as module_0
import zmq.constants as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = ')\\J#xN7Su&iC[-:83A%G'
    int_0 = 366
    dict_0 = {int_0: int_0}
    none_type_0 = None
    z_m_q_designated_receivers_sender_0 = module_0.ZMQDesignatedReceiversSender(dict_0, str_0)
    assert f'{type(z_m_q_designated_receivers_sender_0).__module__}.{type(z_m_q_designated_receivers_sender_0).__qualname__}' == 'snippet_289.ZMQDesignatedReceiversSender'
    assert z_m_q_designated_receivers_sender_0.default_port == {366: 366}
    assert z_m_q_designated_receivers_sender_0.receivers == ')\\J#xN7Su&iC[-:83A%G'
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.NOBLOCK == module_1.Flag.DONTWAIT
    assert module_0.REQ == module_1.SocketType.REQ
    z_m_q_designated_receivers_sender_0.__call__(none_type_0)

def test_case_1():
    float_0 = -1935.5623
    z_m_q_designated_receivers_sender_0 = module_0.ZMQDesignatedReceiversSender(float_0, float_0)
    assert f'{type(z_m_q_designated_receivers_sender_0).__module__}.{type(z_m_q_designated_receivers_sender_0).__qualname__}' == 'snippet_289.ZMQDesignatedReceiversSender'
    assert z_m_q_designated_receivers_sender_0.default_port == pytest.approx(-1935.5623, abs=0.01, rel=0.01)
    assert z_m_q_designated_receivers_sender_0.receivers == pytest.approx(-1935.5623, abs=0.01, rel=0.01)
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.NOBLOCK == module_1.Flag.DONTWAIT
    assert module_0.REQ == module_1.SocketType.REQ

def test_case_2():
    set_0 = set()
    none_type_0 = None
    z_m_q_designated_receivers_sender_0 = module_0.ZMQDesignatedReceiversSender(set_0, set_0)
    assert f'{type(z_m_q_designated_receivers_sender_0).__module__}.{type(z_m_q_designated_receivers_sender_0).__qualname__}' == 'snippet_289.ZMQDesignatedReceiversSender'
    assert z_m_q_designated_receivers_sender_0.default_port == {*()}
    assert z_m_q_designated_receivers_sender_0.receivers == {*()}
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.NOBLOCK == module_1.Flag.DONTWAIT
    assert module_0.REQ == module_1.SocketType.REQ
    z_m_q_designated_receivers_sender_0.__call__(none_type_0)
    z_m_q_designated_receivers_sender_0.close()

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = ')\\J#xN7Su&iC[-:83A%G'
    dict_0 = {str_0: str_0}
    none_type_0 = None
    z_m_q_designated_receivers_sender_0 = module_0.ZMQDesignatedReceiversSender(dict_0, dict_0)
    assert f'{type(z_m_q_designated_receivers_sender_0).__module__}.{type(z_m_q_designated_receivers_sender_0).__qualname__}' == 'snippet_289.ZMQDesignatedReceiversSender'
    assert z_m_q_designated_receivers_sender_0.default_port == {')\\J#xN7Su&iC[-:83A%G': ')\\J#xN7Su&iC[-:83A%G'}
    assert z_m_q_designated_receivers_sender_0.receivers == {')\\J#xN7Su&iC[-:83A%G': ')\\J#xN7Su&iC[-:83A%G'}
    assert module_0.LINGER == module_1.SocketOption.LINGER
    assert module_0.NOBLOCK == module_1.Flag.DONTWAIT
    assert module_0.REQ == module_1.SocketType.REQ
    z_m_q_designated_receivers_sender_0.__call__(none_type_0)