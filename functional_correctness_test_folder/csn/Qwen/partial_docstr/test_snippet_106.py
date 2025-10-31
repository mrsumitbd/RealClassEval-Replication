import pytest
import snippet_106 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b''
    str_0 = "](d$'TWX&xTqC\x0b"
    x_m_l_storage_0 = module_0.XMLStorage()
    assert f'{type(x_m_l_storage_0).__module__}.{type(x_m_l_storage_0).__qualname__}' == 'snippet_106.XMLStorage'
    x_m_l_storage_0.getcoordinates(bytes_0, str_0)