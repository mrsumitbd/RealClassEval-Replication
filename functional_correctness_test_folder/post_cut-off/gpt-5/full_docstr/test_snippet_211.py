import pytest
import snippet_211 as module_0

def test_case_0():
    float_0 = -992.31
    error_handler_0 = module_0.ErrorHandler(float_0)
    assert f'{type(error_handler_0).__module__}.{type(error_handler_0).__qualname__}' == 'snippet_211.ErrorHandler'
    assert error_handler_0.app == pytest.approx(-992.31, abs=0.01, rel=0.01)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '*;5)\\'
    bool_0 = False
    bytes_0 = b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'
    dict_0 = {bytes_0: bytes_0, bytes_0: bytes_0}
    error_handler_0 = module_0.ErrorHandler(dict_0)
    assert f'{type(error_handler_0).__module__}.{type(error_handler_0).__qualname__}' == 'snippet_211.ErrorHandler'
    assert error_handler_0.app == {b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0': b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'}
    error_handler_0.handle_operation_error(str_0, bool_0)