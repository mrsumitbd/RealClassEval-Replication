import pytest
import snippet_321 as module_0

def test_case_0():
    int_0 = 1436
    str_0 = '|Z}s!h,7b>JC@H_'
    registry_config_0 = module_0.RegistryConfig(int_0, int_0, password=int_0, description=str_0)
    assert f'{type(registry_config_0).__module__}.{type(registry_config_0).__qualname__}' == 'snippet_321.RegistryConfig'
    assert registry_config_0.name == 1436
    assert registry_config_0.url == 1436
    assert registry_config_0.user == ''
    assert registry_config_0.password == 1436
    assert registry_config_0.description == '|Z}s!h,7b>JC@H_'
    assert registry_config_0.viewonly is False
    assert module_0.RegistryConfig.user == ''
    assert module_0.RegistryConfig.password == ''
    assert module_0.RegistryConfig.description == ''
    assert module_0.RegistryConfig.viewonly is False
    registry_config_0.to_dict()

def test_case_1():
    none_type_0 = None
    str_0 = 'sXM"\roVhV'
    registry_config_0 = module_0.RegistryConfig(none_type_0, none_type_0, str_0, description=str_0)
    assert f'{type(registry_config_0).__module__}.{type(registry_config_0).__qualname__}' == 'snippet_321.RegistryConfig'
    assert registry_config_0.name is None
    assert registry_config_0.url is None
    assert registry_config_0.user == 'sXM"\roVhV'
    assert registry_config_0.password == ''
    assert registry_config_0.description == 'sXM"\roVhV'
    assert registry_config_0.viewonly is False
    assert module_0.RegistryConfig.user == ''
    assert module_0.RegistryConfig.password == ''
    assert module_0.RegistryConfig.description == ''
    assert module_0.RegistryConfig.viewonly is False
    registry_config_0.to_dict()

def test_case_2():
    bytes_0 = b'\x9d\xa5\xfa\xfcL\x1f\x08\x0evz\xc0\xbbI'
    none_type_0 = None
    str_0 = 'ZuQyJju/-n2\x0bn'
    float_0 = 852.06294
    tuple_0 = ()
    set_0 = {bytes_0}
    registry_config_0 = module_0.RegistryConfig(str_0, tuple_0, password=none_type_0, viewonly=set_0)
    assert f'{type(registry_config_0).__module__}.{type(registry_config_0).__qualname__}' == 'snippet_321.RegistryConfig'
    assert registry_config_0.name == 'ZuQyJju/-n2\x0bn'
    assert registry_config_0.url == ()
    assert registry_config_0.user == ''
    assert registry_config_0.password is None
    assert registry_config_0.description == ''
    assert registry_config_0.viewonly == {b'\x9d\xa5\xfa\xfcL\x1f\x08\x0evz\xc0\xbbI'}
    assert module_0.RegistryConfig.user == ''
    assert module_0.RegistryConfig.password == ''
    assert module_0.RegistryConfig.description == ''
    assert module_0.RegistryConfig.viewonly is False
    str_1 = registry_config_0.__repr__()
    assert str_1 == "RegistryConfig(name='ZuQyJju/-n2\\x0bn', url=(), user='', password='', description='', viewonly={b'\\x9d\\xa5\\xfa\\xfcL\\x1f\\x08\\x0evz\\xc0\\xbbI'})"
    registry_config_1 = module_0.RegistryConfig(bytes_0, bytes_0, str_0, str_0, viewonly=float_0)
    assert f'{type(registry_config_1).__module__}.{type(registry_config_1).__qualname__}' == 'snippet_321.RegistryConfig'
    assert registry_config_1.name == b'\x9d\xa5\xfa\xfcL\x1f\x08\x0evz\xc0\xbbI'
    assert registry_config_1.url == b'\x9d\xa5\xfa\xfcL\x1f\x08\x0evz\xc0\xbbI'
    assert registry_config_1.user == 'ZuQyJju/-n2\x0bn'
    assert registry_config_1.password == 'ZuQyJju/-n2\x0bn'
    assert registry_config_1.description == ''
    assert registry_config_1.viewonly == pytest.approx(852.06294, abs=0.01, rel=0.01)
    str_2 = registry_config_1.__repr__()
    assert str_2 == "RegistryConfig(name=b'\\x9d\\xa5\\xfa\\xfcL\\x1f\\x08\\x0evz\\xc0\\xbbI', url=b'\\x9d\\xa5\\xfa\\xfcL\\x1f\\x08\\x0evz\\xc0\\xbbI', user='ZuQyJju/-n2\\x0bn', password='***MASKED***', description='', viewonly=852.06294)"

def test_case_3():
    str_0 = '9kj'
    registry_config_0 = module_0.RegistryConfig(str_0, str_0, str_0, str_0)
    assert f'{type(registry_config_0).__module__}.{type(registry_config_0).__qualname__}' == 'snippet_321.RegistryConfig'
    assert registry_config_0.name == '9kj'
    assert registry_config_0.url == '9kj'
    assert registry_config_0.user == '9kj'
    assert registry_config_0.password == '9kj'
    assert registry_config_0.description == ''
    assert registry_config_0.viewonly is False
    assert module_0.RegistryConfig.user == ''
    assert module_0.RegistryConfig.password == ''
    assert module_0.RegistryConfig.description == ''
    assert module_0.RegistryConfig.viewonly is False
    str_1 = registry_config_0.__str__()
    assert str_1 == 'Registry config: 9kj at 9kj (user=9kj)'
    registry_config_1 = module_0.RegistryConfig(str_0, str_0, viewonly=str_0)
    assert f'{type(registry_config_1).__module__}.{type(registry_config_1).__qualname__}' == 'snippet_321.RegistryConfig'
    assert registry_config_1.name == '9kj'
    assert registry_config_1.url == '9kj'
    assert registry_config_1.user == ''
    assert registry_config_1.password == ''
    assert registry_config_1.description == ''
    assert registry_config_1.viewonly == '9kj'
    str_2 = registry_config_1.__repr__()
    assert str_2 == "RegistryConfig(name='9kj', url='9kj', user='', password='', description='', viewonly=9kj)"
    str_3 = registry_config_1.__str__()
    assert str_3 == 'Registry config: 9kj at 9kj (no-auth)'