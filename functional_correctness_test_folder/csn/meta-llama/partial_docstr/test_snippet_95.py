import pytest
import snippet_95 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'd'
    module_0.AsyncCmdStep(str_0, str_0)

def test_case_1():
    str_0 = ''
    with pytest.raises(AssertionError):
        module_0.AsyncCmdStep(str_0, str_0)

def test_case_2():
    str_0 = '-]LsxbM\\$;qFVv\x0b'
    none_type_0 = None
    with pytest.raises(AssertionError):
        module_0.AsyncCmdStep(str_0, none_type_0)