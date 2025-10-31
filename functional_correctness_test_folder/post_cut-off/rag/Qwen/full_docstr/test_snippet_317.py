import pytest
import snippet_317 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    web_process_mixin_0 = module_0.WebProcessMixin()
    assert f'{type(web_process_mixin_0).__module__}.{type(web_process_mixin_0).__qualname__}' == 'snippet_317.WebProcessMixin'
    web_process_mixin_0.get_web_ui_pid_path()

@pytest.mark.xfail(strict=True)
def test_case_1():
    web_process_mixin_0 = module_0.WebProcessMixin()
    assert f'{type(web_process_mixin_0).__module__}.{type(web_process_mixin_0).__qualname__}' == 'snippet_317.WebProcessMixin'
    web_process_mixin_0.get_web_ui_expected_start_arg()