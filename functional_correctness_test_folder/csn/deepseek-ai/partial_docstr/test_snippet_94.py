import pytest
import snippet_94 as module_0
import ruamel.yaml.parser as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'j@A\x0b9*m;M[K{Um{~)FN'
    module_0.CmdStep(str_0, str_0)

def test_case_1():
    none_type_0 = None
    with pytest.raises(AssertionError):
        module_0.CmdStep(none_type_0, none_type_0, none_type_0)

def test_case_2():
    var_0 = module_1.xprintf()
    assert f'{type(module_1.annotations).__module__}.{type(module_1.annotations).__qualname__}' == '__future__._Feature'
    assert module_1.annotations.optional == (3, 7, 0, 'beta', 1)
    assert module_1.annotations.mandatory == (3, 11, 0, 'alpha', 0)
    assert module_1.annotations.compiler_flag == 16777216
    assert module_1.SHOW_LINES is False
    assert module_1.C_PRE == 1
    assert module_1.C_POST == 0
    assert module_1.C_SPLIT_ON_FIRST_BLANK == 2

def test_case_3():
    str_0 = 'Y}n>f&c/nA+%d'
    none_type_0 = None
    with pytest.raises(AssertionError):
        module_0.CmdStep(str_0, none_type_0)