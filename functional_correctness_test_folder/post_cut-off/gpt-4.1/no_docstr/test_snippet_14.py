import pytest
import snippet_14 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    float_0 = -3564.27510749746
    module_0.templater(float_0, float_0)