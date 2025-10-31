import pytest
import snippet_15 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'n"1(xop,n'
    module_0._Star(str_0, str_0)