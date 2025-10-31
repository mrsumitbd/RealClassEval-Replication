import pytest
import snippet_294 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    listener_container_0 = module_0.ListenerContainer()
    assert f'{type(listener_container_0).__module__}.{type(listener_container_0).__qualname__}' == 'snippet_294.ListenerContainer'
    assert listener_container_0.listener is None
    assert listener_container_0.output_queue is None
    assert listener_container_0.thread is None
    assert listener_container_0.addresses is None
    assert listener_container_0.nameserver == 'localhost'
    assert f'{type(module_0.ListenerContainer.logger).__module__}.{type(module_0.ListenerContainer.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ListenerContainer.logger.filters == []
    assert module_0.ListenerContainer.logger.name == 'snippet_294.ListenerContainer'
    assert module_0.ListenerContainer.logger.level == 0
    assert f'{type(module_0.ListenerContainer.logger.parent).__module__}.{type(module_0.ListenerContainer.logger.parent).__qualname__}' == 'logging.RootLogger'
    assert module_0.ListenerContainer.logger.propagate is True
    assert module_0.ListenerContainer.logger.handlers == []
    assert module_0.ListenerContainer.logger.disabled is False
    assert f'{type(module_0.ListenerContainer.logger.manager).__module__}.{type(module_0.ListenerContainer.logger.manager).__qualname__}' == 'logging.Manager'
    listener_container_0.restart_listener(listener_container_0)

def test_case_1():
    listener_container_0 = module_0.ListenerContainer()
    assert f'{type(listener_container_0).__module__}.{type(listener_container_0).__qualname__}' == 'snippet_294.ListenerContainer'
    assert listener_container_0.listener is None
    assert listener_container_0.output_queue is None
    assert listener_container_0.thread is None
    assert listener_container_0.addresses is None
    assert listener_container_0.nameserver == 'localhost'
    assert f'{type(module_0.ListenerContainer.logger).__module__}.{type(module_0.ListenerContainer.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ListenerContainer.logger.filters == []
    assert module_0.ListenerContainer.logger.name == 'snippet_294.ListenerContainer'
    assert module_0.ListenerContainer.logger.level == 0
    assert f'{type(module_0.ListenerContainer.logger.parent).__module__}.{type(module_0.ListenerContainer.logger.parent).__qualname__}' == 'logging.RootLogger'
    assert module_0.ListenerContainer.logger.propagate is True
    assert module_0.ListenerContainer.logger.handlers == []
    assert module_0.ListenerContainer.logger.disabled is False
    assert f'{type(module_0.ListenerContainer.logger.manager).__module__}.{type(module_0.ListenerContainer.logger.manager).__qualname__}' == 'logging.Manager'

@pytest.mark.xfail(strict=True)
def test_case_2():
    listener_container_0 = module_0.ListenerContainer()
    assert f'{type(listener_container_0).__module__}.{type(listener_container_0).__qualname__}' == 'snippet_294.ListenerContainer'
    assert listener_container_0.listener is None
    assert listener_container_0.output_queue is None
    assert listener_container_0.thread is None
    assert listener_container_0.addresses is None
    assert listener_container_0.nameserver == 'localhost'
    assert f'{type(module_0.ListenerContainer.logger).__module__}.{type(module_0.ListenerContainer.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ListenerContainer.logger.filters == []
    assert module_0.ListenerContainer.logger.name == 'snippet_294.ListenerContainer'
    assert module_0.ListenerContainer.logger.level == 0
    assert f'{type(module_0.ListenerContainer.logger.parent).__module__}.{type(module_0.ListenerContainer.logger.parent).__qualname__}' == 'logging.RootLogger'
    assert module_0.ListenerContainer.logger.propagate is True
    assert module_0.ListenerContainer.logger.handlers == []
    assert module_0.ListenerContainer.logger.disabled is False
    assert f'{type(module_0.ListenerContainer.logger.manager).__module__}.{type(module_0.ListenerContainer.logger.manager).__qualname__}' == 'logging.Manager'
    listener_container_0.__setstate__(listener_container_0)