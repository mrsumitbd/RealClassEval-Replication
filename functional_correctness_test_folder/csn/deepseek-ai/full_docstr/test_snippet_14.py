import pytest
import snippet_14 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    float_0 = -203.58692139146922
    module_0._Flake(float_0)