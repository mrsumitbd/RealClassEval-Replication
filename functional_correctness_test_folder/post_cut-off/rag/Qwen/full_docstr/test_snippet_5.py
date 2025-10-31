import pytest
import snippet_5 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    script_runner_0 = module_0.ScriptRunner()
    assert f'{type(script_runner_0).__module__}.{type(script_runner_0).__qualname__}' == 'snippet_5.ScriptRunner'
    assert script_runner_0.base_log_path == 'data/local_logs/train.log'
    bool_0 = True
    script_runner_0.execute_script(bool_0, script_runner_0, args=script_runner_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = ':i[&\x0bcC_$-%?+5d'
    script_runner_0 = module_0.ScriptRunner()
    assert f'{type(script_runner_0).__module__}.{type(script_runner_0).__qualname__}' == 'snippet_5.ScriptRunner'
    assert script_runner_0.base_log_path == 'data/local_logs/train.log'
    script_runner_0.execute_script(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    script_runner_0 = module_0.ScriptRunner()
    assert f'{type(script_runner_0).__module__}.{type(script_runner_0).__qualname__}' == 'snippet_5.ScriptRunner'
    assert script_runner_0.base_log_path == 'data/local_logs/train.log'
    script_runner_0.execute_script(script_runner_0, script_runner_0, args=script_runner_0)

def test_case_3():
    script_runner_0 = module_0.ScriptRunner()
    assert f'{type(script_runner_0).__module__}.{type(script_runner_0).__qualname__}' == 'snippet_5.ScriptRunner'
    assert script_runner_0.base_log_path == 'data/local_logs/train.log'