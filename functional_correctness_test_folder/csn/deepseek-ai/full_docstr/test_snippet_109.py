import pytest
import snippet_109 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    history_manager_0 = module_0.HistoryManager()
    assert f'{type(history_manager_0).__module__}.{type(history_manager_0).__qualname__}' == 'snippet_109.HistoryManager'
    assert module_0.TYPE_CHECKING is False
    int_0 = history_manager_0.size()
    assert int_0 == 0
    history_manager_0.reset()
    list_0 = []
    history_manager_0.__call__(list_0)
    history_manager_0.reset()

def test_case_1():
    history_manager_0 = module_0.HistoryManager()
    assert f'{type(history_manager_0).__module__}.{type(history_manager_0).__qualname__}' == 'snippet_109.HistoryManager'
    assert module_0.TYPE_CHECKING is False
    int_0 = history_manager_0.size()
    assert int_0 == 0
    history_manager_0.reset()

def test_case_2():
    bytes_0 = b''
    history_manager_0 = module_0.HistoryManager()
    assert f'{type(history_manager_0).__module__}.{type(history_manager_0).__qualname__}' == 'snippet_109.HistoryManager'
    assert module_0.TYPE_CHECKING is False
    history_manager_0.__call__(bytes_0)