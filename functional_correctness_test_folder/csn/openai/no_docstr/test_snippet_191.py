import pytest
import snippet_191 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '2url\x0bCZ\nX~An0E-\n\\9'
    module_0.AES_GCM_Mechanism(str_0, str_0, str_0)