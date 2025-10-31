import pytest
import snippet_128 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    module_0.GraphPartitioner()

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    module_0.GraphPartitioner(bool_0)