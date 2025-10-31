import pytest
import snippet_222 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = True
    module_0.ModelConfig(bool_0)