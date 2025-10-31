import pytest
import snippet_291 as module_0

def test_case_0():
    module_0.SocketReceiver()

def test_case_1():
    socket_receiver_0 = module_0.SocketReceiver()
    socket_receiver_0.register(socket_receiver_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    socket_receiver_0 = module_0.SocketReceiver()
    socket_receiver_0.unregister(socket_receiver_0)

def test_case_3():
    socket_receiver_0 = module_0.SocketReceiver()
    var_0 = socket_receiver_0.receive()
    socket_receiver_1 = module_0.SocketReceiver()
    with pytest.raises(TimeoutError):
        socket_receiver_1.receive(*var_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    socket_receiver_0 = module_0.SocketReceiver()
    socket_receiver_1 = module_0.SocketReceiver()
    var_0 = socket_receiver_1.receive(timeout=socket_receiver_0)
    socket_receiver_1.receive(*var_0)