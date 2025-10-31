import pytest
import snippet_38 as module_0
import rich.live as module_1

def test_case_0():
    str_0 = 'B64\nC>"^'
    live_display_manager_0 = module_0.LiveDisplayManager(str_0)
    assert f'{type(live_display_manager_0).__module__}.{type(live_display_manager_0).__qualname__}' == 'snippet_38.LiveDisplayManager'
    live_0 = live_display_manager_0.create_live_display()
    assert f'{type(live_0).__module__}.{type(live_0).__qualname__}' == 'rich.live.Live'
    assert live_0.console == 'B64\nC>"^'
    assert live_0.ipy_widget is None
    assert live_0.auto_refresh is True
    assert live_0.transient is False
    assert live_0.refresh_per_second == pytest.approx(0.75, abs=0.01, rel=0.01)
    assert live_0.vertical_overflow == 'visible'
    assert f'{type(module_1.Live.is_started).__module__}.{type(module_1.Live.is_started).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Live.renderable).__module__}.{type(module_1.Live.renderable).__qualname__}' == 'builtins.property'
    str_1 = 'w-58%\\Nxz-4Y\x0c@\t3'
    int_0 = 2558
    live_1 = live_display_manager_0.create_live_display(console=str_1, refresh_per_second=int_0)
    assert f'{type(live_1).__module__}.{type(live_1).__qualname__}' == 'rich.live.Live'
    assert live_1.console == 'w-58%\\Nxz-4Y\x0c@\t3'
    assert live_1.ipy_widget is None
    assert live_1.auto_refresh is True
    assert live_1.transient is False
    assert live_1.refresh_per_second == 2558
    assert live_1.vertical_overflow == 'visible'
    assert f'{type(module_1.annotations).__module__}.{type(module_1.annotations).__qualname__}' == '__future__._Feature'
    assert module_1.annotations.optional == (3, 7, 0, 'beta', 1)
    assert module_1.annotations.mandatory == (3, 11, 0, 'alpha', 0)
    assert module_1.annotations.compiler_flag == 16777216
    assert module_1.TYPE_CHECKING is False

def test_case_1():
    live_display_manager_0 = module_0.LiveDisplayManager()
    assert f'{type(live_display_manager_0).__module__}.{type(live_display_manager_0).__qualname__}' == 'snippet_38.LiveDisplayManager'
    live_0 = live_display_manager_0.create_live_display()
    assert f'{type(live_0).__module__}.{type(live_0).__qualname__}' == 'rich.live.Live'
    assert f'{type(live_0.console).__module__}.{type(live_0.console).__qualname__}' == 'rich.console.Console'
    assert live_0.ipy_widget is None
    assert live_0.auto_refresh is True
    assert live_0.transient is False
    assert live_0.refresh_per_second == pytest.approx(0.75, abs=0.01, rel=0.01)
    assert live_0.vertical_overflow == 'visible'
    assert f'{type(module_1.Live.is_started).__module__}.{type(module_1.Live.is_started).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Live.renderable).__module__}.{type(module_1.Live.renderable).__qualname__}' == 'builtins.property'

def test_case_2():
    live_display_manager_0 = module_0.LiveDisplayManager()
    assert f'{type(live_display_manager_0).__module__}.{type(live_display_manager_0).__qualname__}' == 'snippet_38.LiveDisplayManager'