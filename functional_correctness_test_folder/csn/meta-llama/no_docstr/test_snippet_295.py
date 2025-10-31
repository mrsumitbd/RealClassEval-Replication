import pytest
import snippet_295 as module_0

def test_case_0():
    none_type_0 = None
    designated_receivers_sender_0 = module_0.DesignatedReceiversSender(none_type_0, none_type_0)
    assert f'{type(designated_receivers_sender_0).__module__}.{type(designated_receivers_sender_0).__qualname__}' == 'snippet_295.DesignatedReceiversSender'
    assert f'{type(module_0.config).__module__}.{type(module_0.config).__qualname__}' == 'donfig.config_obj.Config'
    assert module_0.config.name == 'posttroll'
    assert module_0.config.env_prefix == 'POSTTROLL_'
    assert f'{type(module_0.config.env).__module__}.{type(module_0.config.env).__qualname__}' == 'os._Environ'
    assert len(module_0.config.env) == 32
    assert module_0.config.main_path == '/Users/umroot/.config/posttroll'
    assert module_0.config.paths == ['/etc/posttroll', '/opt/anaconda3/envs/pynguin_env/etc/posttroll', '/Users/umroot/.config/posttroll']
    assert module_0.config.defaults == [{'backend': 'unsecure_zmq'}]
    assert module_0.config.deprecations == {}
    assert module_0.config.config == {'backend': 'unsecure_zmq'}
    assert f'{type(module_0.config.config_lock).__module__}.{type(module_0.config.config_lock).__qualname__}' == 'donfig._lock.SerializableLock'

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = -1393
    none_type_0 = None
    designated_receivers_sender_0 = module_0.DesignatedReceiversSender(none_type_0, none_type_0)
    assert f'{type(designated_receivers_sender_0).__module__}.{type(designated_receivers_sender_0).__qualname__}' == 'snippet_295.DesignatedReceiversSender'
    assert f'{type(module_0.config).__module__}.{type(module_0.config).__qualname__}' == 'donfig.config_obj.Config'
    assert module_0.config.name == 'posttroll'
    assert module_0.config.env_prefix == 'POSTTROLL_'
    assert f'{type(module_0.config.env).__module__}.{type(module_0.config.env).__qualname__}' == 'os._Environ'
    assert len(module_0.config.env) == 32
    assert module_0.config.main_path == '/Users/umroot/.config/posttroll'
    assert module_0.config.paths == ['/etc/posttroll', '/opt/anaconda3/envs/pynguin_env/etc/posttroll', '/Users/umroot/.config/posttroll']
    assert module_0.config.defaults == [{'backend': 'unsecure_zmq'}]
    assert module_0.config.deprecations == {}
    assert module_0.config.config == {'backend': 'unsecure_zmq'}
    assert f'{type(module_0.config.config_lock).__module__}.{type(module_0.config.config_lock).__qualname__}' == 'donfig._lock.SerializableLock'
    designated_receivers_sender_0.__call__(int_0)

def test_case_2():
    dict_0 = {}
    designated_receivers_sender_0 = module_0.DesignatedReceiversSender(dict_0, dict_0)
    assert f'{type(designated_receivers_sender_0).__module__}.{type(designated_receivers_sender_0).__qualname__}' == 'snippet_295.DesignatedReceiversSender'
    assert f'{type(module_0.config).__module__}.{type(module_0.config).__qualname__}' == 'donfig.config_obj.Config'
    assert module_0.config.name == 'posttroll'
    assert module_0.config.env_prefix == 'POSTTROLL_'
    assert f'{type(module_0.config.env).__module__}.{type(module_0.config.env).__qualname__}' == 'os._Environ'
    assert len(module_0.config.env) == 32
    assert module_0.config.main_path == '/Users/umroot/.config/posttroll'
    assert module_0.config.paths == ['/etc/posttroll', '/opt/anaconda3/envs/pynguin_env/etc/posttroll', '/Users/umroot/.config/posttroll']
    assert module_0.config.defaults == [{'backend': 'unsecure_zmq'}]
    assert module_0.config.deprecations == {}
    assert module_0.config.config == {'backend': 'unsecure_zmq'}
    assert f'{type(module_0.config.config_lock).__module__}.{type(module_0.config.config_lock).__qualname__}' == 'donfig._lock.SerializableLock'
    none_type_0 = None
    designated_receivers_sender_0.__call__(none_type_0)
    designated_receivers_sender_0.close()