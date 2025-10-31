import pytest
import snippet_26 as module_0
import subprocess as module_1

def test_case_0():
    str_0 = 'IwPdb%Ry9r\n-G}Us'
    system_0 = module_0.System()
    assert f'{type(system_0).__module__}.{type(system_0).__qualname__}' == 'snippet_26.System'
    with pytest.raises(module_1.CalledProcessError):
        system_0.exec_command(str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    system_0 = module_0.System()
    assert f'{type(system_0).__module__}.{type(system_0).__qualname__}' == 'snippet_26.System'
    none_type_0 = None
    system_0.exec_command(none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    float_0 = 307.66767
    str_0 = 'x"=Vh(Go\t'
    system_0 = module_0.System()
    assert f'{type(system_0).__module__}.{type(system_0).__qualname__}' == 'snippet_26.System'
    system_0.create_file(str_0, float_0)

def test_case_3():
    system_0 = module_0.System()
    assert f'{type(system_0).__module__}.{type(system_0).__qualname__}' == 'snippet_26.System'
    str_0 = '$JbV'
    var_0 = system_0.exec_command(str_0, str_0)
    assert var_0 == ''