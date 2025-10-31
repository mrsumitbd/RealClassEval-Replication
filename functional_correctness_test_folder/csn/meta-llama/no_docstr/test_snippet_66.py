import pytest
import snippet_66 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '"('
    module_0.ArgumentProcessor(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = ''
    module_0.ArgumentProcessor(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b''
    list_0 = [bytes_0, bytes_0, bytes_0]
    module_0.ArgumentProcessor(bytes_0, list_0)