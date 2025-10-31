import pytest
import snippet_105 as module_0

def test_case_0():
    code_language_registry_0 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_0).__module__}.{type(code_language_registry_0).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_0.language_configs == {}

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '2rKv7"m P*{h/'
    code_language_registry_0 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_0).__module__}.{type(code_language_registry_0).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_0.language_configs == {}
    none_type_0 = code_language_registry_0.register(str_0, str_0)
    assert code_language_registry_0.language_configs == {'2rKv7"m P*{h/': '2rKv7"m P*{h/'}
    code_language_registry_1 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_1).__module__}.{type(code_language_registry_1).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_1.language_configs == {}
    bool_0 = code_language_registry_0.__contains__(code_language_registry_1)
    assert bool_0 is False
    code_language_registry_1.__getitem__(str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = 'o2(r'
    code_language_registry_0 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_0).__module__}.{type(code_language_registry_0).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_0.language_configs == {}
    code_language_registry_0.get(str_0)

def test_case_3():
    code_language_registry_0 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_0).__module__}.{type(code_language_registry_0).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_0.language_configs == {}
    str_0 = '+`-/Rt,\t0f%O/e'
    bool_0 = code_language_registry_0.__contains__(str_0)
    assert bool_0 is False

@pytest.mark.xfail(strict=True)
def test_case_4():
    code_language_registry_0 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_0).__module__}.{type(code_language_registry_0).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_0.language_configs == {}
    code_language_registry_1 = module_0._CodeLanguageRegistry()
    assert f'{type(code_language_registry_1).__module__}.{type(code_language_registry_1).__qualname__}' == 'snippet_105._CodeLanguageRegistry'
    assert code_language_registry_1.language_configs == {}
    bool_0 = code_language_registry_0.__contains__(code_language_registry_1)
    assert bool_0 is False
    code_language_registry_0.keys()
    code_language_registry_0.__getitem__(code_language_registry_1)