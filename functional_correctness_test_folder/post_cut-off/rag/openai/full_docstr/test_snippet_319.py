import pytest
import snippet_319 as module_0

def test_case_0():
    task_manager_0 = module_0.TaskManager()
    assert f'{type(task_manager_0).__module__}.{type(task_manager_0).__qualname__}' == 'snippet_319.TaskManager'
    assert f'{type(task_manager_0.executor).__module__}.{type(task_manager_0.executor).__qualname__}' == 'concurrent.futures.thread.ThreadPoolExecutor'
    assert task_manager_0.tasks == {}
    assert task_manager_0.futures == {}
    task_manager_0.run_task(task_manager_0)

def test_case_1():
    task_manager_0 = module_0.TaskManager()
    assert f'{type(task_manager_0).__module__}.{type(task_manager_0).__qualname__}' == 'snippet_319.TaskManager'
    assert f'{type(task_manager_0.executor).__module__}.{type(task_manager_0.executor).__qualname__}' == 'concurrent.futures.thread.ThreadPoolExecutor'
    assert task_manager_0.tasks == {}
    assert task_manager_0.futures == {}

def test_case_2():
    task_manager_0 = module_0.TaskManager()
    assert f'{type(task_manager_0).__module__}.{type(task_manager_0).__qualname__}' == 'snippet_319.TaskManager'
    assert f'{type(task_manager_0.executor).__module__}.{type(task_manager_0.executor).__qualname__}' == 'concurrent.futures.thread.ThreadPoolExecutor'
    assert task_manager_0.tasks == {}
    assert task_manager_0.futures == {}
    str_0 = task_manager_0.run_task(task_manager_0)
    task_manager_0.get_task(str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    task_manager_0 = module_0.TaskManager()
    assert f'{type(task_manager_0).__module__}.{type(task_manager_0).__qualname__}' == 'snippet_319.TaskManager'
    assert f'{type(task_manager_0.executor).__module__}.{type(task_manager_0.executor).__qualname__}' == 'concurrent.futures.thread.ThreadPoolExecutor'
    assert task_manager_0.tasks == {}
    assert task_manager_0.futures == {}
    task_manager_0.run_task(task_manager_0)
    task_manager_0.shutdown()