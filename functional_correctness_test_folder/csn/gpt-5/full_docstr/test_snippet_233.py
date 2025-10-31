import pytest
import snippet_233 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = -2181
    template_0 = module_0.Template(int_0, int_0)
    assert f'{type(template_0).__module__}.{type(template_0).__qualname__}' == 'snippet_233.Template'
    assert template_0.name == -2181
    template_0.get_version()

@pytest.mark.xfail(strict=True)
def test_case_1():
    complex_0 = 303.198353 - 3938j
    none_type_0 = None
    template_0 = module_0.Template(none_type_0, none_type_0)
    assert f'{type(template_0).__module__}.{type(template_0).__qualname__}' == 'snippet_233.Template'
    assert template_0.name is None
    template_0.get_version(complex_0)

def test_case_2():
    none_type_0 = None
    template_0 = module_0.Template(none_type_0, none_type_0)
    assert f'{type(template_0).__module__}.{type(template_0).__qualname__}' == 'snippet_233.Template'
    assert template_0.name is None

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    template_0 = module_0.Template(none_type_0, none_type_0)
    assert f'{type(template_0).__module__}.{type(template_0).__qualname__}' == 'snippet_233.Template'
    assert template_0.name is None
    template_0.get_latest_version()

@pytest.mark.xfail(strict=True)
def test_case_4():
    bytes_0 = b'\xe6u\xaaCE>@\x93\xba/\x04u\xb6~BR9T\xe6m'
    dict_0 = {bytes_0: bytes_0, bytes_0: bytes_0, bytes_0: bytes_0, bytes_0: bytes_0}
    bool_0 = True
    template_0 = module_0.Template(bool_0, dict_0)
    assert f'{type(template_0).__module__}.{type(template_0).__qualname__}' == 'snippet_233.Template'
    assert template_0.name is True
    template_0.get_latest_version()