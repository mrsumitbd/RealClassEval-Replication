import pytest
import snippet_210 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = ' 9.``"QR:4\x0bzd5'
    module_0.EnumDefinition(str_0, str_0)