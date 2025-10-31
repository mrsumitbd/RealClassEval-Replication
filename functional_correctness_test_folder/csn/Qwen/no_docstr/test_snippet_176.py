import pytest
import snippet_176 as module_0
import enum as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\xd6$\x05\x89\xa3|a\x05\xe9\x8fs\xfdI\x0e\x8f\x00'
    modder_0 = module_0.Modder(bytes_0)
    assert f'{type(modder_0).__module__}.{type(modder_0).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_0.supported_actions).__module__}.{type(modder_0.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_0.supported_actions) == 6
    assert modder_0.strict is True
    assert modder_0.directory == './'
    modder_1 = module_0.Modder()
    assert f'{type(modder_1).__module__}.{type(modder_1).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_1.supported_actions).__module__}.{type(modder_1.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_1.supported_actions) == 10
    assert modder_1.strict is True
    assert modder_1.directory == './'
    modder_1.modify_object(modder_1, modder_1)

def test_case_1():
    modder_0 = module_0.Modder()
    assert f'{type(modder_0).__module__}.{type(modder_0).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_0.supported_actions).__module__}.{type(modder_0.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_0.supported_actions) == 10
    assert modder_0.strict is True
    assert modder_0.directory == './'

@pytest.mark.xfail(strict=True)
def test_case_2():
    modder_0 = module_0.Modder()
    assert f'{type(modder_0).__module__}.{type(modder_0).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_0.supported_actions).__module__}.{type(modder_0.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_0.supported_actions) == 10
    assert modder_0.strict is True
    assert modder_0.directory == './'
    modder_0.modify_object(modder_0, modder_0)

def test_case_3():
    modder_0 = module_0.Modder()
    assert f'{type(modder_0).__module__}.{type(modder_0).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_0.supported_actions).__module__}.{type(modder_0.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_0.supported_actions) == 10
    assert modder_0.strict is True
    assert modder_0.directory == './'
    enum_dict_0 = module_1._EnumDict()
    assert f'{type(enum_dict_0).__module__}.{type(enum_dict_0).__qualname__}' == 'enum._EnumDict'
    assert len(enum_dict_0) == 0
    modder_0.modify(enum_dict_0, enum_dict_0)

def test_case_4():
    float_0 = 1350.562
    dict_0 = {float_0: float_0}
    modder_0 = module_0.Modder(strict=dict_0)
    assert f'{type(modder_0).__module__}.{type(modder_0).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_0.supported_actions).__module__}.{type(modder_0.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_0.supported_actions) == 10
    assert f'{type(modder_0.strict).__module__}.{type(modder_0.strict).__qualname__}' == 'builtins.dict'
    assert len(modder_0.strict) == 1
    assert modder_0.directory == './'
    with pytest.raises(ValueError):
        modder_0.modify(dict_0, modder_0)

def test_case_5():
    float_0 = 1348.8233233230922
    dict_0 = {float_0: float_0}
    none_type_0 = None
    modder_0 = module_0.Modder(strict=none_type_0, directory=dict_0)
    assert f'{type(modder_0).__module__}.{type(modder_0).__qualname__}' == 'snippet_176.Modder'
    assert f'{type(modder_0.supported_actions).__module__}.{type(modder_0.supported_actions).__qualname__}' == 'builtins.dict'
    assert len(modder_0.supported_actions) == 10
    assert modder_0.strict is None
    assert f'{type(modder_0.directory).__module__}.{type(modder_0.directory).__qualname__}' == 'builtins.dict'
    assert len(modder_0.directory) == 1
    modder_0.modify(dict_0, modder_0)