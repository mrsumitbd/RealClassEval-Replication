import pytest
import snippet_51 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'kgaSFPvfU)vM~I*`i'
    module_0.Array(str_0)

def test_case_1():
    bytes_0 = b''
    array_0 = module_0.Array(bytes_0)
    assert f'{type(array_0).__module__}.{type(array_0).__qualname__}' == 'snippet_51.Array'
    array_0.__call__(bytes_0)