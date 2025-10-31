import pytest
import snippet_296 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    str_0 = 'r1|_v#\t)-Q\x0cYWQ'
    name_server_0 = module_0.NameServer(multicast_enabled=none_type_0)
    assert f'{type(name_server_0).__module__}.{type(name_server_0).__qualname__}' == 'snippet_296.NameServer'
    assert name_server_0.loop is True
    assert name_server_0.listener is None
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
    none_type_1 = None
    name_server_1 = module_0.NameServer(str_0, restrict_to_localhost=none_type_1)
    assert f'{type(name_server_1).__module__}.{type(name_server_1).__qualname__}' == 'snippet_296.NameServer'
    assert name_server_1.loop is True
    assert name_server_1.listener is None
    name_server_0.run(name_server_0)

def test_case_1():
    name_server_0 = module_0.NameServer()
    assert f'{type(name_server_0).__module__}.{type(name_server_0).__qualname__}' == 'snippet_296.NameServer'
    assert name_server_0.loop is True
    assert name_server_0.listener is None
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
def test_case_2():
    name_server_0 = module_0.NameServer()
    assert f'{type(name_server_0).__module__}.{type(name_server_0).__qualname__}' == 'snippet_296.NameServer'
    assert name_server_0.loop is True
    assert name_server_0.listener is None
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
    name_server_0.run(nameserver_address=name_server_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = ','
    name_server_0 = module_0.NameServer()
    assert f'{type(name_server_0).__module__}.{type(name_server_0).__qualname__}' == 'snippet_296.NameServer'
    assert name_server_0.loop is True
    assert name_server_0.listener is None
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
    name_server_0.run(str_0, name_server_0)

def test_case_4():
    none_type_0 = None
    name_server_0 = module_0.NameServer(multicast_enabled=none_type_0)
    assert f'{type(name_server_0).__module__}.{type(name_server_0).__qualname__}' == 'snippet_296.NameServer'
    assert name_server_0.loop is True
    assert name_server_0.listener is None
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
    name_server_0.stop()