import pytest
import snippet_16 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    module_0._Trail(bool_0, bool_0)