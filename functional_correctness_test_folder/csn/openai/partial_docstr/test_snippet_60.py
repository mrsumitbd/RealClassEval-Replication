import pytest
import snippet_60 as module_0

def test_case_0():
    int_0 = -1077
    code_page_manager_0 = module_0.CodePageManager(int_0)
    assert f'{type(code_page_manager_0).__module__}.{type(code_page_manager_0).__qualname__}' == 'snippet_60.CodePageManager'
    assert code_page_manager_0.data == -1077

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    none_type_1 = None
    code_page_manager_0 = module_0.CodePageManager(none_type_1)
    assert f'{type(code_page_manager_0).__module__}.{type(code_page_manager_0).__qualname__}' == 'snippet_60.CodePageManager'
    assert code_page_manager_0.data is None
    code_page_manager_0.get_encoding_name(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b'w\xac\xae\x10\xae\xcb\x1d\xd4\xa6\xd0K\xfa?\xb2\\\xb5|c\xd6'
    bytes_1 = b'\xdd<\xe9\xd8v9=\x15\x0e\x0cs\xd3'
    code_page_manager_0 = module_0.CodePageManager(bytes_1)
    assert f'{type(code_page_manager_0).__module__}.{type(code_page_manager_0).__qualname__}' == 'snippet_60.CodePageManager'
    assert code_page_manager_0.data == b'\xdd<\xe9\xd8v9=\x15\x0e\x0cs\xd3'
    code_page_manager_0.get_encoding(bytes_0)