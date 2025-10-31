import pytest
import snippet_111 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    module_0.Connection()