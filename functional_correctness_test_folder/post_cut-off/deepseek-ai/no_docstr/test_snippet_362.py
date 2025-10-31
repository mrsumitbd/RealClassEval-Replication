import pytest
import snippet_362 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    module_0.ScriptRunner()

def test_case_1():
    str_0 = '\x0c[:gi'
    script_runner_0 = module_0.ScriptRunner(str_0)
    assert f'{type(script_runner_0).__module__}.{type(script_runner_0).__qualname__}' == 'snippet_362.ScriptRunner'
    assert script_runner_0.compiler == '\x0c[:gi'
    script_runner_0.list_scripts()

def test_case_2():
    str_0 = 'q9\rDE<~4AZuQK\x0c2'
    script_runner_0 = module_0.ScriptRunner(str_0)
    assert f'{type(script_runner_0).__module__}.{type(script_runner_0).__qualname__}' == 'snippet_362.ScriptRunner'
    assert script_runner_0.compiler == 'q9\rDE<~4AZuQK\x0c2'
    with pytest.raises(RuntimeError):
        script_runner_0.run_script(str_0, str_0)