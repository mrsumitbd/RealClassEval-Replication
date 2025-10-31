import pytest
import snippet_174 as module_0

def test_case_0():
    subscriber_0 = module_0.Subscriber()
    assert f'{type(subscriber_0).__module__}.{type(subscriber_0).__qualname__}' == 'snippet_174.Subscriber'
    with pytest.raises(NotImplementedError):
        subscriber_0.update_property(subscriber_0)

def test_case_1():
    subscriber_0 = module_0.Subscriber()
    assert f'{type(subscriber_0).__module__}.{type(subscriber_0).__qualname__}' == 'snippet_174.Subscriber'
    with pytest.raises(NotImplementedError):
        subscriber_0.update_action(subscriber_0)

def test_case_2():
    subscriber_0 = module_0.Subscriber()
    assert f'{type(subscriber_0).__module__}.{type(subscriber_0).__qualname__}' == 'snippet_174.Subscriber'
    with pytest.raises(NotImplementedError):
        subscriber_0.update_event(subscriber_0)