import pytest
import snippet_198 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'zKx(H_`,bIVE%@@k&P'
    shortcuts_command_0 = module_0.ShortcutsCommand()
    assert f'{type(shortcuts_command_0).__module__}.{type(shortcuts_command_0).__qualname__}' == 'snippet_198.ShortcutsCommand'
    shortcuts_command_0.run(str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    shortcuts_command_0 = module_0.ShortcutsCommand()
    assert f'{type(shortcuts_command_0).__module__}.{type(shortcuts_command_0).__qualname__}' == 'snippet_198.ShortcutsCommand'
    shortcuts_command_0.run()

def test_case_2():
    shortcuts_command_0 = module_0.ShortcutsCommand()
    assert f'{type(shortcuts_command_0).__module__}.{type(shortcuts_command_0).__qualname__}' == 'snippet_198.ShortcutsCommand'