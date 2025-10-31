import pytest
import snippet_64 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'Jju/-n2\x0b'
    module_0.FastTextAug(str_0)