import pytest
import snippet_28 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    module_0.DistanceData(none_type_0, none_type_0)