import pytest
import snippet_71 as module_0

def test_case_0():
    none_type_0 = None
    hook_event_0 = module_0.HookEvent(none_type_0)
    assert f'{type(hook_event_0).__module__}.{type(hook_event_0).__qualname__}' == 'snippet_71.HookEvent'
    assert hook_event_0.agent is None
    assert module_0.TYPE_CHECKING is False
    assert f'{type(module_0.HookEvent.should_reverse_callbacks).__module__}.{type(module_0.HookEvent.should_reverse_callbacks).__qualname__}' == 'builtins.property'
    with pytest.raises(AttributeError):
        hook_event_0.__setattr__(hook_event_0, hook_event_0)

def test_case_1():
    none_type_0 = None
    hook_event_0 = module_0.HookEvent(none_type_0)
    assert f'{type(hook_event_0).__module__}.{type(hook_event_0).__qualname__}' == 'snippet_71.HookEvent'
    assert hook_event_0.agent is None
    assert module_0.TYPE_CHECKING is False
    assert f'{type(module_0.HookEvent.should_reverse_callbacks).__module__}.{type(module_0.HookEvent.should_reverse_callbacks).__qualname__}' == 'builtins.property'