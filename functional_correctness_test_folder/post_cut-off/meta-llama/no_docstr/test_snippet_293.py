import pytest
import snippet_293 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'M.\x0bUv\x0cK9f'
    module_0.KNNModel(str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    list_0 = []
    module_0.KNNModel(list_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    int_0 = -518
    module_0.KNNModel(int_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    bytes_0 = b'\xa4V'
    set_0 = {bytes_0, bytes_0}
    module_0.KNNModel(set_0, bytes_0)