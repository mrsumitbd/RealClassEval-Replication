import pytest
import snippet_296 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    module_0.BenchmarkVisualizer()

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    module_0.BenchmarkVisualizer(dict_0)