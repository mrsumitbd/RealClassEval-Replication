import pytest
import snippet_298 as module_0

def test_case_0():
    session_manager_port_0 = module_0.SessionManagerPort()
    assert f'{type(session_manager_port_0).__module__}.{type(session_manager_port_0).__qualname__}' == 'snippet_298.SessionManagerPort'
    with pytest.raises(NotImplementedError):
        session_manager_port_0.get_session()

def test_case_1():
    session_manager_port_0 = module_0.SessionManagerPort()
    assert f'{type(session_manager_port_0).__module__}.{type(session_manager_port_0).__qualname__}' == 'snippet_298.SessionManagerPort'
    with pytest.raises(NotImplementedError):
        session_manager_port_0.remove_session()